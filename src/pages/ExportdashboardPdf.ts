/**
 * exportDashboardPDF.ts
 *
 * Generates a styled, printable HTML report from dashboard data
 * and opens the browser's Print → Save as PDF dialog.
 *
 * Usage in Dashboard.tsx:
 *   import { exportDashboardPDF } from "@/lib/exportDashboardPDF";
 *
 *   const handleExport = () =>
 *     exportDashboardPDF({ dateRange, kpis, quickInsights });
 *   // radarCategories, monthlySavings, marketplaceRejections, styleDistribution
 *   // are optional — pass live data if you have it, otherwise defaults are used.
 */

export interface KpiRow {
  label: string;
  value: string;
  change: number;
  status?: string;
  isLive?: boolean;
}

export interface QuickInsight {
  type: "success" | "warning" | "info";
  message: string;
}

export interface RadarCategory {
  category: string;
  imageMismatch: number;
  attrMismatch: number;
  lowResolution: number;
  missingKeywords: number;
}

export interface MonthlySaving {
  month: string;
  savingsINR: number;
}

export interface MarketplaceRejection {
  marketplace: string;
  rejectionRate: number;
  skuCount: number;
}

export interface StyleCard {
  style: string;
  count: number;
  growth: number;
}

export interface ExportPayload {
  dateRange: string;
  kpis: KpiRow[];
  quickInsights: QuickInsight[];
  /** Optional live chart data — defaults are used if not provided */
  radarCategories?: RadarCategory[];
  monthlySavings?: MonthlySaving[];
  marketplaceRejections?: MarketplaceRejection[];
  styleDistribution?: StyleCard[];
}

// ── Default chart data (mirrors what the dashboard renders) ──────────────────

const DEFAULT_RADAR: RadarCategory[] = [
  { category: "Beauty",      imageMismatch: 56, attrMismatch: 39, lowResolution: 22, missingKeywords: 33 },
  { category: "Electronics", imageMismatch: 56, attrMismatch: 67, lowResolution:  8, missingKeywords: 44 },
  { category: "Fashion",     imageMismatch: 53, attrMismatch: 60, lowResolution: 33, missingKeywords: 47 },
  { category: "Grocery",     imageMismatch: 54, attrMismatch: 69, lowResolution: 46, missingKeywords: 38 },
  { category: "Home",        imageMismatch:  8, attrMismatch: 38, lowResolution: 15, missingKeywords: 54 },
];

const DEFAULT_SAVINGS: MonthlySaving[] = [
  { month: "Nov", savingsINR:  90_300 },
  { month: "Dec", savingsINR: 107_300 },
  { month: "Jan", savingsINR:  42_100 },
  { month: "Feb", savingsINR:  58_500 },
  { month: "Mar", savingsINR:  41_600 },
  { month: "Apr", savingsINR:  95_700 },
];

const DEFAULT_REJECTIONS: MarketplaceRejection[] = [
  { marketplace: "Amazon.com",  rejectionRate: 10, skuCount:  88 },
  { marketplace: "Amazon.in",   rejectionRate: 13, skuCount:  81 },
  { marketplace: "Checkers",    rejectionRate:  8, skuCount:  85 },
  { marketplace: "Flipkart",    rejectionRate:  9, skuCount:  84 },
  { marketplace: "Magento",     rejectionRate:  7, skuCount:  92 },
  { marketplace: "Makro",       rejectionRate:  9, skuCount:  79 },
  { marketplace: "Myntra",      rejectionRate: 10, skuCount:  94 },
  { marketplace: "Shopify",     rejectionRate:  5, skuCount:  82 },
  { marketplace: "Takealot",    rejectionRate:  6, skuCount:  61 },
  { marketplace: "Walmart",     rejectionRate: 12, skuCount:  83 },
  { marketplace: "WooCommerce", rejectionRate:  6, skuCount:  68 },
  { marketplace: "Woolworths",  rejectionRate:  7, skuCount: 101 },
  { marketplace: "eBay",        rejectionRate: 16, skuCount:  74 },
];

const DEFAULT_STYLES: StyleCard[] = [
  { style: "Studio",    count: 46_100, growth:  8 },
  { style: "Flat Lay",  count: 37_550, growth: 22 },
  { style: "Lifestyle", count: 21_450, growth: 15 },
];

// ── Helpers ──────────────────────────────────────────────────────────────────

const DATE_LABEL: Record<string, string> = {
  "7d":  "vs previous 7 days",
  "30d": "vs previous 30 days",
  "90d": "vs previous 90 days",
  "1y":  "vs previous year",
};

function fmtINR(val: number): string {
  if (val >= 1_00_000) return `₹${(val / 1_00_000).toFixed(1)}L`;
  if (val >= 1_000)    return `₹${(val / 1_000).toFixed(1)}K`;
  return `₹${val}`;
}

function changeChip(change: number): string {
  const color = change >= 0 ? "#16a34a" : "#dc2626";
  const arrow = change >= 0 ? "▲" : "▼";
  return `<span style="color:${color};font-weight:600">${arrow} ${Math.abs(change)}%</span>`;
}

function statusBadge(status = ""): string {
  const map: Record<string, { bg: string; text: string }> = {
    success: { bg: "#dcfce7", text: "#166534" },
    warning: { bg: "#fef9c3", text: "#92400e" },
    danger:  { bg: "#fee2e2", text: "#991b1b" },
    info:    { bg: "#dbeafe", text: "#1e40af" },
  };
  const style = map[status] ?? { bg: "#f1f5f9", text: "#475569" };
  return `<span style="display:inline-block;padding:2px 10px;border-radius:20px;
    font-size:11px;font-weight:600;background:${style.bg};color:${style.text}">${status || "—"}</span>`;
}

function riskColor(pct: number): string {
  if (pct < 40) return "#16a34a";
  if (pct < 70) return "#d97706";
  return "#dc2626";
}

function insightIcon(type: string): string {
  if (type === "success") return "✅";
  if (type === "warning") return "⚠️";
  return "💡";
}

// ── Section builders ──────────────────────────────────────────────────────────

function insightsSection(insights: QuickInsight[]): string {
  const rows = insights
    .map(
      (ins) => `<tr>
        <td style="width:40px;text-align:center;font-size:16px">${insightIcon(ins.type)}</td>
        <td>${ins.message}</td>
      </tr>`
    )
    .join("");
  return `
  <h2>Quick Insights</h2>
  <table>
    <thead><tr><th style="width:40px">Type</th><th>Message</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function kpiTable(kpis: KpiRow[]): string {
  const rows = kpis
    .map(
      (k) => `<tr>
        <td>${k.label}</td>
        <td><strong>${k.value}</strong></td>
        <td>${changeChip(k.change)}</td>
        <td>${statusBadge(k.status)}</td>
        <td><span style="font-size:11px;padding:2px 8px;border-radius:12px;
          background:${k.isLive ? "#dcfce7" : "#f1f5f9"};
          color:${k.isLive ? "#166534" : "#64748b"};font-weight:600">
          ${k.isLive ? "Live" : "Demo"}</span></td>
      </tr>`
    )
    .join("");
  return `
  <h2>Key Performance Indicators</h2>
  <table>
    <thead><tr><th>Metric</th><th>Value</th><th>Change</th><th>Status</th><th>Source</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function radarTable(categories: RadarCategory[]): string {
  const rows = categories
    .map((cat) => {
      const avg = (
        (cat.imageMismatch + cat.attrMismatch + cat.lowResolution + cat.missingKeywords) / 4
      ).toFixed(2);
      const cell = (v: number) =>
        `<td style="color:${riskColor(v)};font-weight:600">${v}%</td>`;
      return `<tr>
        <td><strong>${cat.category}</strong></td>
        ${cell(cat.imageMismatch)}${cell(cat.attrMismatch)}${cell(cat.lowResolution)}${cell(cat.missingKeywords)}
        <td>${avg}%</td>
      </tr>`;
    })
    .join("");
  return `
  <h2>Content Quality Risk Radar</h2>
  <p style="font-size:12px;color:#64748b;margin:-4px 0 10px">
    Issue distribution by category — risk legend:
    <span style="color:#16a34a;font-weight:600">● Low (&lt;40%)</span>
    <span style="color:#d97706;font-weight:600;margin-left:8px">● Medium (40–70%)</span>
    <span style="color:#dc2626;font-weight:600;margin-left:8px">● High (&gt;70%)</span>
  </p>
  <table>
    <thead><tr>
      <th>Category</th><th>Image Mismatch</th><th>Attribute Mismatch</th>
      <th>Low Resolution</th><th>Missing Keywords</th><th>Avg Risk</th>
    </tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function savingsTable(savings: MonthlySaving[]): string {
  const total = savings.reduce((s, r) => s + r.savingsINR, 0);
  const rows = savings
    .map((s) => `<tr><td>${s.month}</td><td>${fmtINR(s.savingsINR)}</td></tr>`)
    .join("");
  return `
  <h2>AI Photoshoot — Monthly Cost Savings</h2>
  <table>
    <thead><tr><th>Month</th><th>Savings (₹)</th></tr></thead>
    <tbody>${rows}</tbody>
    <tfoot><tr style="font-weight:700;background:#f8fafc">
      <td>Total</td><td>${fmtINR(total)}</td>
    </tr></tfoot>
  </table>`;
}

function rejectionTable(data: MarketplaceRejection[]): string {
  const sorted = [...data].sort((a, b) => b.rejectionRate - a.rejectionRate);
  const rows = sorted
    .map(
      (mp) => `<tr>
        <td>${mp.marketplace}</td>
        <td style="color:${riskColor(mp.rejectionRate * 2)};font-weight:600">${mp.rejectionRate}%</td>
        <td>${mp.skuCount.toLocaleString("en-IN")} SKUs</td>
      </tr>`
    )
    .join("");
  return `
  <h2>AI Photoshoot — Rejection Rate by Marketplace</h2>
  <table>
    <thead><tr><th>Marketplace</th><th>Rejection Rate</th><th>SKU Count</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function styleTable(styles: StyleCard[]): string {
  const rows = styles
    .map(
      (s) => `<tr>
        <td>${s.style}</td>
        <td>${s.count.toLocaleString("en-IN")}</td>
        <td style="color:${s.growth >= 0 ? "#16a34a" : "#dc2626"};font-weight:600">
          ${s.growth >= 0 ? "▲" : "▼"} ${Math.abs(s.growth)}%
        </td>
      </tr>`
    )
    .join("");
  return `
  <h2>AI Photoshoot — Style Distribution</h2>
  <table>
    <thead><tr><th>Style</th><th>Count</th><th>Growth</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

// ── Main export function ──────────────────────────────────────────────────────

export function exportDashboardPDF(payload: ExportPayload): void {
  const {
    dateRange,
    kpis,
    quickInsights,
    // Use passed-in live data, or fall back to the default data that mirrors the dashboard
    radarCategories     = DEFAULT_RADAR,
    monthlySavings      = DEFAULT_SAVINGS,
    marketplaceRejections = DEFAULT_REJECTIONS,
    styleDistribution   = DEFAULT_STYLES,
  } = payload;

  const now = new Date().toLocaleString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const periodLabel = DATE_LABEL[dateRange] ?? dateRange;

  const sections = [
    insightsSection(quickInsights),
    kpiTable(kpis),
    radarTable(radarCategories),
    savingsTable(monthlySavings),
    rejectionTable(marketplaceRejections),
    styleTable(styleDistribution),
  ].join("\n");

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Content Intel Dashboard Export</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
      background:#f8fafc;color:#1e293b;padding:32px;
    }
    .header-bar{
      display:flex;align-items:center;gap:14px;
      border-bottom:3px solid #6366f1;padding-bottom:18px;margin-bottom:6px;
    }
    .logo{
      width:44px;height:44px;border-radius:12px;
      background:linear-gradient(135deg,#6366f1,#8b5cf6);
      display:flex;align-items:center;justify-content:center;
      font-size:22px;flex-shrink:0;
    }
    h1{font-size:24px;font-weight:800;color:#0f172a;line-height:1.2}
    .sub{font-size:12px;color:#64748b;margin-top:2px}
    .meta{font-size:13px;color:#64748b;margin:10px 0 24px}
    .meta strong{color:#1e293b}
    h2{
      font-size:15px;font-weight:700;color:#0f172a;
      margin:30px 0 10px;padding-bottom:6px;
      border-bottom:2px solid #e2e8f0;
    }
    table{
      width:100%;border-collapse:collapse;background:#fff;
      border-radius:10px;overflow:hidden;
      box-shadow:0 1px 4px rgba(0,0,0,.08);font-size:13px;
    }
    th{
      background:#f1f5f9;color:#475569;font-weight:600;
      text-align:left;padding:10px 14px;border-bottom:1px solid #e2e8f0;
    }
    td{padding:9px 14px;border-bottom:1px solid #f1f5f9;color:#334155}
    tfoot td{padding:10px 14px;border-top:2px solid #e2e8f0;background:#f8fafc}
    tr:last-child td{border-bottom:none}
    tr:hover td{background:#f8fafc}
    .footer{
      margin-top:36px;padding-top:14px;border-top:1px solid #e2e8f0;
      font-size:12px;color:#94a3b8;text-align:center;
    }
    @media print{
      body{background:#fff;padding:16px}
      table{box-shadow:none}
      h2{page-break-before:auto}
    }
  </style>
</head>
<body>
  <div class="header-bar">
    <div class="logo">📊</div>
    <div>
      <h1>AI E-Commerce Content Intelligence</h1>
      <div class="sub">Global Command Center • Real-time content accuracy • AI imagery • Marketplace compliance</div>
    </div>
  </div>
  <p class="meta">
    Export period: <strong>${periodLabel}</strong>
    &nbsp;|&nbsp;
    Generated: <strong>${now}</strong>
  </p>

  ${sections}

  <div class="footer">Content Intel &nbsp;•&nbsp; Exported ${now}</div>

  <script>
    window.onload = function() { window.print(); };
  <\/script>
</body>
</html>`;

  const blob = new Blob([html], { type: "text/html;charset=utf-8" });
  const url  = URL.createObjectURL(blob);
  const win  = window.open(url, "_blank");
  if (!win) {
    // Popup blocked fallback — trigger download of the HTML file instead
    const a = document.createElement("a");
    a.href = url;
    a.download = `content-intel-dashboard-${dateRange}-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
  // Clean up the object URL after a delay
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}