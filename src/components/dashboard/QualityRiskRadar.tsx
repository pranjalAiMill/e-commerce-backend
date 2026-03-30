// // // import { useState } from "react";
// // // import { useQuery } from "@tanstack/react-query";
// // // import { cn } from "@/lib/utils";
// // // import { toast } from "@/hooks/use-toast";
// // // import { apiClient } from "@/lib/api";
// // // import { Badge } from "@/components/ui/badge";
// // // import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
// // // import { AlertCircle, TrendingUp, TrendingDown } from "lucide-react";

// // // type IssueType = "Image Mismatch" | "Attribute Error" | "Low Resolution" | "Missing Keywords";

// // // interface QualityRiskRadarResponse {
// // //   riskData: Record<string, Record<IssueType, number>>;
// // //   categories: string[];
// // //   issueTypes: IssueType[];
// // // }

// // // function getRiskColor(value: number) {
// // //   if (value >= 70) return "text-destructive";
// // //   if (value >= 40) return "text-warning";
// // //   return "text-success";
// // // }

// // // function getRiskBg(value: number) {
// // //   if (value >= 70) return "bg-destructive";
// // //   if (value >= 40) return "bg-warning";
// // //   return "bg-success";
// // // }

// // // function getRiskIntensity(value: number): "high" | "medium" | "low" {
// // //   if (value >= 70) return "high";
// // //   if (value >= 40) return "medium";
// // //   return "low";
// // // }

// // // export function QualityRiskRadar() {
// // //   const [selectedMarketplace, setSelectedMarketplace] = useState("Amazon.in");

// // //   const { data, isLoading, isError } = useQuery<QualityRiskRadarResponse>({
// // //     queryKey: ["dashboard", "quality-risk-radar", selectedMarketplace],
// // //     queryFn: () =>
// // //       apiClient.get<QualityRiskRadarResponse>(
// // //         `/dashboard/quality-risk-radar?marketplace=${encodeURIComponent(selectedMarketplace)}`,
// // //       ),
// // //   });

// // //   // Fallback dummy data
// // //   const dummyCategories = ["Fashion", "Beauty", "Electronics", "Home", "Grocery"];
// // //   const dummyIssueTypes: IssueType[] = ["Image Mismatch", "Attribute Error", "Low Resolution", "Missing Keywords"];
// // //   const dummyRiskData: Record<string, Record<IssueType, number>> = {
// // //     "Fashion": { "Image Mismatch": 85, "Attribute Error": 45, "Low Resolution": 20, "Missing Keywords": 60 },
// // //     "Beauty": { "Image Mismatch": 30, "Attribute Error": 70, "Low Resolution": 15, "Missing Keywords": 40 },
// // //     "Electronics": { "Image Mismatch": 15, "Attribute Error": 25, "Low Resolution": 80, "Missing Keywords": 35 },
// // //     "Home": { "Image Mismatch": 50, "Attribute Error": 55, "Low Resolution": 30, "Missing Keywords": 75 },
// // //     "Grocery": { "Image Mismatch": 25, "Attribute Error": 40, "Low Resolution": 10, "Missing Keywords": 90 },
// // //   };

// // //   const categories = data?.categories.length ? data.categories : dummyCategories;
// // //   const issueTypes = data?.issueTypes.length ? data.issueTypes : dummyIssueTypes;
// // //   const riskData = data?.riskData && Object.keys(data.riskData).length > 0 ? data.riskData : dummyRiskData;
// // //   const isUsingDummy = isError || (!data && !isLoading);

// // //   return (
// // //     <TooltipProvider>
// // //       <div className="glass-card rounded-xl p-8 opacity-0 animate-fade-in" style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}>
// // //         <div className="flex items-start justify-between mb-8">
// // //           <div className="space-y-1">
// // //             <div className="flex items-center gap-3">
// // //               <h3 className="text-2xl font-bold text-foreground tracking-tight">Content Quality Risk Radar</h3>
// // //               {data ? (
// // //                 <Badge variant="default" className="text-[10px] px-2 py-0.5 bg-success/20 text-success border-success/30 font-medium">
// // //                   Live
// // //                 </Badge>
// // //               ) : isError ? (
// // //                 <Badge variant="outline" className="text-[10px] px-2 py-0.5 text-muted-foreground border-muted font-medium">
// // //                   Demo
// // //                 </Badge>
// // //               ) : null}
// // //             </div>
// // //             <p className="text-sm text-muted-foreground">Issue distribution by category with risk levels</p>
// // //           </div>
// // //           <div className="flex gap-3 text-xs bg-muted/50 p-2 rounded-lg">
// // //             <div className="flex items-center gap-2">
// // //               <div className="w-3 h-3 rounded bg-success" />
// // //               <span className="text-muted-foreground font-medium">Low (&lt;40%)</span>
// // //             </div>
// // //             <div className="flex items-center gap-2">
// // //               <div className="w-3 h-3 rounded bg-warning" />
// // //               <span className="text-muted-foreground font-medium">Medium (40-70%)</span>
// // //             </div>
// // //             <div className="flex items-center gap-2">
// // //               <div className="w-3 h-3 rounded bg-destructive" />
// // //               <span className="text-muted-foreground font-medium">High (&gt;70%)</span>
// // //             </div>
// // //           </div>
// // //         </div>

// // //         <div className="space-y-6">
// // //           {isLoading && categories.length === 0 && (
// // //             <>
// // //               {Array.from({ length: 5 }).map((_, rowIdx) => (
// // //                 <div key={rowIdx} className="space-y-2">
// // //                   <div className="h-4 w-24 bg-muted rounded animate-pulse" />
// // //                   <div className="grid grid-cols-4 gap-3">
// // //                     {Array.from({ length: 4 }).map((_, colIdx) => (
// // //                       <div key={colIdx} className="h-16 rounded-lg bg-muted animate-pulse" />
// // //                     ))}
// // //                   </div>
// // //                 </div>
// // //               ))}
// // //             </>
// // //           )}
// // //           {categories.map((category) => (
// // //             <div key={category} className="space-y-3">
// // //               <div className="flex items-center justify-between">
// // //                 <h4 className="text-base font-semibold text-foreground">{category}</h4>
// // //                 <span className="text-xs text-muted-foreground">
// // //                   {Object.values(riskData[category] || {}).reduce((sum, val) => sum + val, 0) / issueTypes.length}% avg
// // //                 </span>
// // //               </div>
// // //               <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
// // //                 {issueTypes.map((type) => {
// // //                   const value = riskData[category]?.[type] ?? 0;
// // //                   const intensity = getRiskIntensity(value);
// // //                   return (
// // //                     <Tooltip key={type}>
// // //                       <TooltipTrigger asChild>
// // //                         <div 
// // //                           className={cn(
// // //                             "heat-cell p-4 border border-border/50 rounded-xl",
// // //                             "hover:border-opacity-100 transition-all cursor-pointer",
// // //                             intensity === "high" && "bg-destructive/5 border-destructive/20",
// // //                             intensity === "medium" && "bg-warning/5 border-warning/20",
// // //                             intensity === "low" && "bg-success/5 border-success/20"
// // //                           )}
// // //                           role="button"
// // //                           tabIndex={0}
// // //                           aria-label={`${category} - ${type}: ${value}%`}
// // //                         >
// // //                           <div className="flex items-center justify-between mb-2">
// // //                             <span className="text-xs font-medium text-muted-foreground truncate pr-2">
// // //                               {type}
// // //                             </span>
// // //                             <span className={cn(
// // //                               "text-sm font-bold tabular-nums",
// // //                               getRiskColor(value)
// // //                             )}>
// // //                               {value}%
// // //                             </span>
// // //                           </div>
// // //                           <div className="progress-bar">
// // //                             <div 
// // //                               className={cn(
// // //                                 "progress-fill",
// // //                                 getRiskBg(value)
// // //                               )}
// // //                               style={{ width: `${value}%` }}
// // //                               aria-valuenow={value}
// // //                               aria-valuemin={0}
// // //                               aria-valuemax={100}
// // //                               role="progressbar"
// // //                             />
// // //                           </div>
// // //                         </div>
// // //                       </TooltipTrigger>
// // //                       <TooltipContent>
// // //                         <p className="font-medium">{category} - {type}</p>
// // //                         <p className="text-xs text-muted-foreground mt-1">
// // //                           Risk Level: {intensity.toUpperCase()} ({value}%)
// // //                         </p>
// // //                       </TooltipContent>
// // //                     </Tooltip>
// // //                   );
// // //                 })}
// // //               </div>
// // //             </div>
// // //           ))}
// // //         </div>

// // //         <div className="mt-6 pt-6 border-t border-border/50">
// // //           <div className="flex items-center justify-between">
// // //             <span className="text-sm font-medium text-muted-foreground">Filter by Marketplace</span>
// // //             <div className="flex gap-2">
// // //               {["Amazon.in", "Flipkart", "Takealot"].map((mp) => (
// // //                 <button
// // //                   key={mp}
// // //                   onClick={() => {
// // //                     setSelectedMarketplace(mp);
// // //                     toast({
// // //                       title: "Marketplace changed",
// // //                       description: `Viewing data for ${mp}`,
// // //                     });
// // //                   }}
// // //                   className={cn(
// // //                     "px-4 py-2 text-xs font-semibold rounded-lg transition-all",
// // //                     "hover:scale-105 active:scale-95",
// // //                     selectedMarketplace === mp
// // //                       ? "bg-primary text-primary-foreground shadow-sm"
// // //                       : "bg-muted text-muted-foreground hover:bg-muted/80"
// // //                   )}
// // //                   aria-pressed={selectedMarketplace === mp}
// // //                   aria-label={`Filter by ${mp}`}
// // //                 >
// // //                   {mp}
// // //                 </button>
// // //               ))}
// // //             </div>
// // //           </div>
// // //         </div>
// // //       </div>
// // //     </TooltipProvider>
// // //   );
// // // }


// // import { useState } from "react";
// // import { useQuery } from "@tanstack/react-query";
// // import { cn } from "@/lib/utils";
// // import { toast } from "@/hooks/use-toast";
// // import { Badge } from "@/components/ui/badge";
// // import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
// // import { Loader2 } from "lucide-react";

// // const EXEC_API_BASE = import.meta.env.VITE_MISMATCH_API_URL ?? "http://127.0.0.1:8011";

// // // ── Types ──────────────────────────────────────────────────────────────────

// // type IssueType = "Image Mismatch" | "Attribute Error" | "Low Resolution" | "Missing Keywords";

// // interface QualityRiskRadarResponse {
// //   riskData: Record<string, Record<IssueType, number>>;
// //   categories: string[];
// //   issueTypes: IssueType[];
// // }

// // interface RiskRadarRaw {
// //   data: {
// //     category: string;
// //     avg: number;
// //     issues: { type: string; value: number }[];
// //   }[];
// //   marketplaces: string[];
// // }

// // // ── Helpers ────────────────────────────────────────────────────────────────

// // function getRiskColor(value: number) {
// //   if (value >= 70) return "text-destructive";
// //   if (value >= 40) return "text-warning";
// //   return "text-success";
// // }

// // function getRiskBg(value: number) {
// //   if (value >= 70) return "bg-destructive";
// //   if (value >= 40) return "bg-warning";
// //   return "bg-success";
// // }

// // function getRiskIntensity(value: number): "high" | "medium" | "low" {
// //   if (value >= 70) return "high";
// //   if (value >= 40) return "medium";
// //   return "low";
// // }

// // // Maps backend type names → frontend IssueType keys
// // const TYPE_MAP: Record<string, IssueType> = {
// //   "Image Mismatch":     "Image Mismatch",
// //   "Attribute Mismatch": "Attribute Error",
// //   "Low Resolution":     "Low Resolution",
// //   "Missing Keywords":   "Missing Keywords",
// // };

// // const ISSUE_TYPES: IssueType[] = [
// //   "Image Mismatch",
// //   "Attribute Error",
// //   "Low Resolution",
// //   "Missing Keywords",
// // ];

// // function transformRiskRadar(raw: RiskRadarRaw): QualityRiskRadarResponse {
// //   const riskData: Record<string, Record<IssueType, number>> = {};

// //   for (const cat of raw.data) {
// //     const row: Record<IssueType, number> = {
// //       "Image Mismatch":   0,
// //       "Attribute Error":  0,
// //       "Low Resolution":   0,
// //       "Missing Keywords": 0,
// //     };
// //     for (const issue of cat.issues) {
// //       const key = TYPE_MAP[issue.type];
// //       if (key) row[key] = issue.value;
// //     }
// //     riskData[cat.category] = row;
// //   }

// //   return {
// //     categories: raw.data.map((d) => d.category),
// //     issueTypes: ISSUE_TYPES,
// //     riskData,
// //   };
// // }

// // // ── Component ──────────────────────────────────────────────────────────────

// // export function QualityRiskRadar() {
// //   // Default to no marketplace filter — shows all categories across all marketplaces
// //   const [selectedMarketplace, setSelectedMarketplace] = useState<string | null>(null);

// //   const { data: raw, isLoading, isError, error } = useQuery<RiskRadarRaw>({
// //     queryKey: ["executive", "risk-radar", selectedMarketplace],
// //     queryFn: async () => {
// //       const params = new URLSearchParams();
// //       if (selectedMarketplace) params.set("marketplace", selectedMarketplace);
// //       const url = `${EXEC_API_BASE}/executive/risk-radar?${params.toString()}`;
// //       const res = await fetch(url);
// //       if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
// //       return res.json();
// //     },
// //     retry: 1,
// //     staleTime: 30_000,
// //   });

// //   // Always use live data when available, never silently fall back
// //   const transformed   = raw ? transformRiskRadar(raw) : null;
// //   const categories    = transformed?.categories ?? [];
// //   const issueTypes    = transformed?.issueTypes ?? ISSUE_TYPES;
// //   const riskData      = transformed?.riskData   ?? {};

// //   // Marketplace buttons — always from API
// //   const marketplaceButtons = raw?.marketplaces ?? [];

// //   const isLive = !!raw && !isError;

// //   return (
// //     <TooltipProvider>
// //       <div
// //         className="glass-card rounded-xl p-8 opacity-0 animate-fade-in"
// //         style={{ animationDelay: "200ms", animationFillMode: "forwards" }}
// //       >
// //         {/* ── Header ── */}
// //         <div className="flex items-start justify-between mb-8">
// //           <div className="space-y-1">
// //             <div className="flex items-center gap-3">
// //               <h3 className="text-2xl font-bold text-foreground tracking-tight">
// //                 Content Quality Risk Radar
// //               </h3>
// //               {isLoading ? (
// //                 <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
// //               ) : isLive ? (
// //                 <Badge
// //                   variant="default"
// //                   className="text-[10px] px-2 py-0.5 bg-success/20 text-success border-success/30 font-medium"
// //                 >
// //                   Live
// //                 </Badge>
// //               ) : isError ? (
// //                 <Badge
// //                   variant="outline"
// //                   className="text-[10px] px-2 py-0.5 text-destructive border-destructive/30 font-medium"
// //                 >
// //                   API Error
// //                 </Badge>
// //               ) : null}
// //             </div>
// //             <p className="text-sm text-muted-foreground">
// //               Issue distribution by category with risk levels
// //               {selectedMarketplace && (
// //                 <span className="ml-1 font-medium text-foreground">
// //                   — {selectedMarketplace}
// //                 </span>
// //               )}
// //             </p>
// //           </div>

// //           {/* Legend */}
// //           <div className="flex gap-3 text-xs bg-muted/50 p-2 rounded-lg">
// //             <div className="flex items-center gap-2">
// //               <div className="w-3 h-3 rounded bg-success" />
// //               <span className="text-muted-foreground font-medium">Low (&lt;40%)</span>
// //             </div>
// //             <div className="flex items-center gap-2">
// //               <div className="w-3 h-3 rounded bg-warning" />
// //               <span className="text-muted-foreground font-medium">Medium (40-70%)</span>
// //             </div>
// //             <div className="flex items-center gap-2">
// //               <div className="w-3 h-3 rounded bg-destructive" />
// //               <span className="text-muted-foreground font-medium">High (&gt;70%)</span>
// //             </div>
// //           </div>
// //         </div>

// //         {/* ── Error state ── */}
// //         {isError && (
// //           <div className="mb-6 p-4 rounded-lg bg-destructive/5 border border-destructive/20 text-sm text-destructive">
// //             Failed to load data from backend ({String(error)}).
// //             Make sure your backend is running on <code className="font-mono">{EXEC_API_BASE}</code>.
// //           </div>
// //         )}

// //         {/* ── Skeleton while loading ── */}
// //         {isLoading && (
// //           <div className="space-y-6">
// //             {Array.from({ length: 5 }).map((_, rowIdx) => (
// //               <div key={rowIdx} className="space-y-2">
// //                 <div className="h-4 w-24 bg-muted rounded animate-pulse" />
// //                 <div className="grid grid-cols-4 gap-3">
// //                   {Array.from({ length: 4 }).map((_, colIdx) => (
// //                     <div key={colIdx} className="h-16 rounded-lg bg-muted animate-pulse" />
// //                   ))}
// //                 </div>
// //               </div>
// //             ))}
// //           </div>
// //         )}

// //         {/* ── Category rows (only when we have live data) ── */}
// //         {!isLoading && categories.length > 0 && (
// //           <div className="space-y-6">
// //             {categories.map((category) => {
// //               const catValues = Object.values(riskData[category] || {});
// //               const avg = catValues.length > 0
// //                 ? (catValues.reduce((s, v) => s + v, 0) / catValues.length).toFixed(2)
// //                 : "0";

// //               return (
// //                 <div key={category} className="space-y-3">
// //                   <div className="flex items-center justify-between">
// //                     <h4 className="text-base font-semibold text-foreground">{category}</h4>
// //                     <span className="text-xs text-muted-foreground">{avg}% avg</span>
// //                   </div>
// //                   <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
// //                     {issueTypes.map((type) => {
// //                       const value     = riskData[category]?.[type] ?? 0;
// //                       const intensity = getRiskIntensity(value);
// //                       return (
// //                         <Tooltip key={type}>
// //                           <TooltipTrigger asChild>
// //                             <div
// //                               className={cn(
// //                                 "heat-cell p-4 border border-border/50 rounded-xl",
// //                                 "hover:border-opacity-100 transition-all cursor-pointer",
// //                                 intensity === "high"   && "bg-destructive/5 border-destructive/20",
// //                                 intensity === "medium" && "bg-warning/5 border-warning/20",
// //                                 intensity === "low"    && "bg-success/5 border-success/20"
// //                               )}
// //                               role="button"
// //                               tabIndex={0}
// //                               aria-label={`${category} - ${type}: ${value}%`}
// //                             >
// //                               <div className="flex items-center justify-between mb-2">
// //                                 <span className="text-xs font-medium text-muted-foreground truncate pr-2">
// //                                   {type}
// //                                 </span>
// //                                 <span className={cn("text-sm font-bold tabular-nums", getRiskColor(value))}>
// //                                   {value}%
// //                                 </span>
// //                               </div>
// //                               <div className="progress-bar">
// //                                 <div
// //                                   className={cn("progress-fill", getRiskBg(value))}
// //                                   style={{ width: `${value}%` }}
// //                                   aria-valuenow={value}
// //                                   aria-valuemin={0}
// //                                   aria-valuemax={100}
// //                                   role="progressbar"
// //                                 />
// //                               </div>
// //                             </div>
// //                           </TooltipTrigger>
// //                           <TooltipContent>
// //                             <p className="font-medium">{category} - {type}</p>
// //                             <p className="text-xs text-muted-foreground mt-1">
// //                               Risk Level: {intensity.toUpperCase()} ({value}%)
// //                             </p>
// //                           </TooltipContent>
// //                         </Tooltip>
// //                       );
// //                     })}
// //                   </div>
// //                 </div>
// //               );
// //             })}
// //           </div>
// //         )}

// //         {/* ── Empty state when no categories returned ── */}
// //         {!isLoading && !isError && categories.length === 0 && (
// //           <div className="text-center py-12 text-sm text-muted-foreground">
// //             No data available for the selected filters.
// //           </div>
// //         )}

// //         {/* ── Marketplace filter buttons ── */}
// //         <div className="mt-6 pt-6 border-t border-border/50">
// //           <div className="flex items-center justify-between flex-wrap gap-3">
// //             <span className="text-sm font-medium text-muted-foreground">
// //               Filter by Marketplace
// //             </span>
// //             <div className="flex flex-wrap gap-2">
// //               {/* "All" button */}
// //               <button
// //                 onClick={() => {
// //                   setSelectedMarketplace(null);
// //                   toast({ title: "Marketplace filter cleared", description: "Showing all marketplaces" });
// //                 }}
// //                 className={cn(
// //                   "px-4 py-2 text-xs font-semibold rounded-lg transition-all",
// //                   "hover:scale-105 active:scale-95",
// //                   selectedMarketplace === null
// //                     ? "bg-primary text-primary-foreground shadow-sm"
// //                     : "bg-muted text-muted-foreground hover:bg-muted/80"
// //                 )}
// //               >
// //                 All
// //               </button>

// //               {/* Dynamic marketplace buttons from API */}
// //               {marketplaceButtons.map((mp) => (
// //                 <button
// //                   key={mp}
// //                   onClick={() => {
// //                     setSelectedMarketplace(mp);
// //                     toast({
// //                       title: "Marketplace changed",
// //                       description: `Viewing data for ${mp}`,
// //                     });
// //                   }}
// //                   className={cn(
// //                     "px-4 py-2 text-xs font-semibold rounded-lg transition-all",
// //                     "hover:scale-105 active:scale-95",
// //                     selectedMarketplace === mp
// //                       ? "bg-primary text-primary-foreground shadow-sm"
// //                       : "bg-muted text-muted-foreground hover:bg-muted/80"
// //                   )}
// //                   aria-pressed={selectedMarketplace === mp}
// //                   aria-label={`Filter by ${mp}`}
// //                 >
// //                   {mp}
// //                 </button>
// //               ))}

// //               {/* Fallback buttons if API hasn't loaded yet */}
// //               {marketplaceButtons.length === 0 && isLoading && (
// //                 ["Amazon.in", "Flipkart", "Takealot"].map((mp) => (
// //                   <div key={mp} className="h-8 w-20 bg-muted rounded-lg animate-pulse" />
// //                 ))
// //               )}
// //             </div>
// //           </div>
// //         </div>
// //       </div>
// //     </TooltipProvider>
// //   );
// // }

// import { useState } from "react";
// import { useQuery } from "@tanstack/react-query";
// import { cn } from "@/lib/utils";
// import { toast } from "@/hooks/use-toast";
// import { Badge } from "@/components/ui/badge";
// import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
// import { Loader2 } from "lucide-react";

// const EXEC_API_BASE = import.meta.env.VITE_MISMATCH_API_URL ?? "http://127.0.0.1:8011";

// // ── Types ──────────────────────────────────────────────────────────────────

// type IssueType = "Image Mismatch" | "Attribute Error" | "Low Resolution" | "Missing Keywords";

// interface QualityRiskRadarResponse {
//   riskData: Record<string, Record<IssueType, number>>;
//   categories: string[];
//   issueTypes: IssueType[];
// }

// interface RiskRadarRaw {
//   data: {
//     category: string;
//     avg: number;
//     issues: { type: string; value: number }[];
//   }[];
//   marketplaces: string[];
// }

// interface QualityRiskRadarProps {
//   dateRange?: string;
// }

// // ── Helpers ────────────────────────────────────────────────────────────────

// function getRiskColor(value: number) {
//   if (value >= 70) return "text-destructive";
//   if (value >= 40) return "text-warning";
//   return "text-success";
// }

// function getRiskBg(value: number) {
//   if (value >= 70) return "bg-destructive";
//   if (value >= 40) return "bg-warning";
//   return "bg-success";
// }

// function getRiskIntensity(value: number): "high" | "medium" | "low" {
//   if (value >= 70) return "high";
//   if (value >= 40) return "medium";
//   return "low";
// }

// const TYPE_MAP: Record<string, IssueType> = {
//   "Image Mismatch":     "Image Mismatch",
//   "Attribute Mismatch": "Attribute Error",
//   "Low Resolution":     "Low Resolution",
//   "Missing Keywords":   "Missing Keywords",
// };

// const ISSUE_TYPES: IssueType[] = [
//   "Image Mismatch",
//   "Attribute Error",
//   "Low Resolution",
//   "Missing Keywords",
// ];

// function transformRiskRadar(raw: RiskRadarRaw): QualityRiskRadarResponse {
//   const riskData: Record<string, Record<IssueType, number>> = {};

//   for (const cat of raw.data) {
//     const row: Record<IssueType, number> = {
//       "Image Mismatch":   0,
//       "Attribute Error":  0,
//       "Low Resolution":   0,
//       "Missing Keywords": 0,
//     };
//     for (const issue of cat.issues) {
//       const key = TYPE_MAP[issue.type];
//       if (key) row[key] = issue.value;
//     }
//     riskData[cat.category] = row;
//   }

//   return {
//     categories: raw.data.map((d) => d.category),
//     issueTypes: ISSUE_TYPES,
//     riskData,
//   };
// }

// // ── Component ──────────────────────────────────────────────────────────────

// export function QualityRiskRadar({ dateRange = "30d" }: QualityRiskRadarProps) {
//   const [selectedMarketplace, setSelectedMarketplace] = useState<string | null>(null);

//   const { data: raw, isLoading, isError, error } = useQuery<RiskRadarRaw>({
//     queryKey: ["executive", "risk-radar", selectedMarketplace, dateRange],
//     queryFn: async () => {
//       const params = new URLSearchParams();
//       if (selectedMarketplace) params.set("marketplace", selectedMarketplace);
//       // FIX: backend Query param is "period", not "date_range"
//       params.set("period", dateRange);
//       const url = `${EXEC_API_BASE}/executive/risk-radar?${params.toString()}`;
//       const res = await fetch(url);
//       if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
//       return res.json();
//     },
//     retry: 1,
//     staleTime: 30_000,
//   });

//   const transformed        = raw ? transformRiskRadar(raw) : null;
//   const categories         = transformed?.categories ?? [];
//   const issueTypes         = transformed?.issueTypes ?? ISSUE_TYPES;
//   const riskData           = transformed?.riskData   ?? {};
//   const marketplaceButtons = raw?.marketplaces ?? [];
//   const isLive             = !!raw && !isError;

//   return (
//     <TooltipProvider>
//       <div
//         className="glass-card rounded-xl p-8 opacity-0 animate-fade-in"
//         style={{ animationDelay: "200ms", animationFillMode: "forwards" }}
//       >
//         {/* ── Header ── */}
//         <div className="flex items-start justify-between mb-8">
//           <div className="space-y-1">
//             <div className="flex items-center gap-3">
//               <h3 className="text-2xl font-bold text-foreground tracking-tight">
//                 Content Quality Risk Radar
//               </h3>
//               {isLoading ? (
//                 <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
//               ) : isLive ? (
//                 <Badge
//                   variant="default"
//                   className="text-[10px] px-2 py-0.5 bg-success/20 text-success border-success/30 font-medium"
//                 >
//                   Live
//                 </Badge>
//               ) : isError ? (
//                 <Badge
//                   variant="outline"
//                   className="text-[10px] px-2 py-0.5 text-destructive border-destructive/30 font-medium"
//                 >
//                   API Error
//                 </Badge>
//               ) : null}
//             </div>
//             <p className="text-sm text-muted-foreground">
//               Issue distribution by category with risk levels
//               {selectedMarketplace && (
//                 <span className="ml-1 font-medium text-foreground">
//                   — {selectedMarketplace}
//                 </span>
//               )}
//             </p>
//           </div>

//           {/* Legend */}
//           <div className="flex gap-3 text-xs bg-muted/50 p-2 rounded-lg">
//             <div className="flex items-center gap-2">
//               <div className="w-3 h-3 rounded bg-success" />
//               <span className="text-muted-foreground font-medium">Low (&lt;40%)</span>
//             </div>
//             <div className="flex items-center gap-2">
//               <div className="w-3 h-3 rounded bg-warning" />
//               <span className="text-muted-foreground font-medium">Medium (40-70%)</span>
//             </div>
//             <div className="flex items-center gap-2">
//               <div className="w-3 h-3 rounded bg-destructive" />
//               <span className="text-muted-foreground font-medium">High (&gt;70%)</span>
//             </div>
//           </div>
//         </div>

//         {/* ── Error state ── */}
//         {isError && (
//           <div className="mb-6 p-4 rounded-lg bg-destructive/5 border border-destructive/20 text-sm text-destructive">
//             Failed to load data from backend ({String(error)}).
//             Make sure your backend is running on <code className="font-mono">{EXEC_API_BASE}</code>.
//           </div>
//         )}

//         {/* ── Skeleton while loading ── */}
//         {isLoading && (
//           <div className="space-y-6">
//             {Array.from({ length: 5 }).map((_, rowIdx) => (
//               <div key={rowIdx} className="space-y-2">
//                 <div className="h-4 w-24 bg-muted rounded animate-pulse" />
//                 <div className="grid grid-cols-4 gap-3">
//                   {Array.from({ length: 4 }).map((_, colIdx) => (
//                     <div key={colIdx} className="h-16 rounded-lg bg-muted animate-pulse" />
//                   ))}
//                 </div>
//               </div>
//             ))}
//           </div>
//         )}

//         {/* ── Category rows ── */}
//         {!isLoading && categories.length > 0 && (
//           <div className="space-y-6">
//             {categories.map((category) => {
//               const catValues = Object.values(riskData[category] || {});
//               const avg = catValues.length > 0
//                 ? (catValues.reduce((s, v) => s + v, 0) / catValues.length).toFixed(2)
//                 : "0";

//               return (
//                 <div key={category} className="space-y-3">
//                   <div className="flex items-center justify-between">
//                     <h4 className="text-base font-semibold text-foreground">{category}</h4>
//                     <span className="text-xs text-muted-foreground">{avg}% avg</span>
//                   </div>
//                   <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
//                     {issueTypes.map((type) => {
//                       const value     = riskData[category]?.[type] ?? 0;
//                       const intensity = getRiskIntensity(value);
//                       return (
//                         <Tooltip key={type}>
//                           <TooltipTrigger asChild>
//                             <div
//                               className={cn(
//                                 "heat-cell p-4 border border-border/50 rounded-xl",
//                                 "hover:border-opacity-100 transition-all cursor-pointer",
//                                 intensity === "high"   && "bg-destructive/5 border-destructive/20",
//                                 intensity === "medium" && "bg-warning/5 border-warning/20",
//                                 intensity === "low"    && "bg-success/5 border-success/20"
//                               )}
//                               role="button"
//                               tabIndex={0}
//                               aria-label={`${category} - ${type}: ${value}%`}
//                             >
//                               <div className="flex items-center justify-between mb-2">
//                                 <span className="text-xs font-medium text-muted-foreground truncate pr-2">
//                                   {type}
//                                 </span>
//                                 <span className={cn("text-sm font-bold tabular-nums", getRiskColor(value))}>
//                                   {value}%
//                                 </span>
//                               </div>
//                               <div className="progress-bar">
//                                 <div
//                                   className={cn("progress-fill", getRiskBg(value))}
//                                   style={{ width: `${value}%` }}
//                                   aria-valuenow={value}
//                                   aria-valuemin={0}
//                                   aria-valuemax={100}
//                                   role="progressbar"
//                                 />
//                               </div>
//                             </div>
//                           </TooltipTrigger>
//                           <TooltipContent>
//                             <p className="font-medium">{category} - {type}</p>
//                             <p className="text-xs text-muted-foreground mt-1">
//                               Risk Level: {intensity.toUpperCase()} ({value}%)
//                             </p>
//                           </TooltipContent>
//                         </Tooltip>
//                       );
//                     })}
//                   </div>
//                 </div>
//               );
//             })}
//           </div>
//         )}

//         {/* ── Empty state ── */}
//         {!isLoading && !isError && categories.length === 0 && (
//           <div className="text-center py-12 text-sm text-muted-foreground">
//             No data available for the selected filters.
//           </div>
//         )}

//         {/* ── Marketplace filter buttons ── */}
//         <div className="mt-6 pt-6 border-t border-border/50">
//           <div className="flex items-center justify-between flex-wrap gap-3">
//             <span className="text-sm font-medium text-muted-foreground">
//               Filter by Marketplace
//             </span>
//             <div className="flex flex-wrap gap-2">
//               <button
//                 onClick={() => {
//                   setSelectedMarketplace(null);
//                   toast({ title: "Marketplace filter cleared", description: "Showing all marketplaces" });
//                 }}
//                 className={cn(
//                   "px-4 py-2 text-xs font-semibold rounded-lg transition-all",
//                   "hover:scale-105 active:scale-95",
//                   selectedMarketplace === null
//                     ? "bg-primary text-primary-foreground shadow-sm"
//                     : "bg-muted text-muted-foreground hover:bg-muted/80"
//                 )}
//               >
//                 All
//               </button>

//               {marketplaceButtons.map((mp) => (
//                 <button
//                   key={mp}
//                   onClick={() => {
//                     setSelectedMarketplace(mp);
//                     toast({ title: "Marketplace changed", description: `Viewing data for ${mp}` });
//                   }}
//                   className={cn(
//                     "px-4 py-2 text-xs font-semibold rounded-lg transition-all",
//                     "hover:scale-105 active:scale-95",
//                     selectedMarketplace === mp
//                       ? "bg-primary text-primary-foreground shadow-sm"
//                       : "bg-muted text-muted-foreground hover:bg-muted/80"
//                   )}
//                   aria-pressed={selectedMarketplace === mp}
//                   aria-label={`Filter by ${mp}`}
//                 >
//                   {mp}
//                 </button>
//               ))}

//               {marketplaceButtons.length === 0 && isLoading && (
//                 ["Amazon.in", "Flipkart", "Takealot"].map((mp) => (
//                   <div key={mp} className="h-8 w-20 bg-muted rounded-lg animate-pulse" />
//                 ))
//               )}
//             </div>
//           </div>
//         </div>
//       </div>
//     </TooltipProvider>
//   );
// }

import { useState, useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Loader2 } from "lucide-react";

const EXEC_API_BASE = import.meta.env.VITE_MISMATCH_API_URL ?? "e-commerce-dashboard-asapc3eac9b9dfb7.westus2-01.azurewebsites.net";

// ── Types ──────────────────────────────────────────────────────────────────

type IssueType = "Image Mismatch" | "Attribute Error" | "Low Resolution" | "Missing Keywords";

interface RiskRadarRaw {
  data: {
    category: string;
    avg: number;
    issues: { type: string; value: number }[];
  }[];
  marketplaces: string[];
}

interface TransformedRadar {
  categories: string[];
  issueTypes: IssueType[];
  riskData: Record<string, Record<IssueType, number>>;
}

interface QualityRiskRadarProps {
  dateRange?: string;
}

// ── Helpers ────────────────────────────────────────────────────────────────

function getRiskColor(value: number) {
  if (value >= 70) return "text-destructive";
  if (value >= 40) return "text-warning";
  return "text-success";
}

function getRiskBg(value: number) {
  if (value >= 70) return "bg-destructive";
  if (value >= 40) return "bg-warning";
  return "bg-success";
}

function getRiskIntensity(value: number): "high" | "medium" | "low" {
  if (value >= 70) return "high";
  if (value >= 40) return "medium";
  return "low";
}

const TYPE_MAP: Record<string, IssueType> = {
  "Image Mismatch":     "Image Mismatch",
  "Attribute Mismatch": "Attribute Error",
  "Low Resolution":     "Low Resolution",
  "Missing Keywords":   "Missing Keywords",
};

const ISSUE_TYPES: IssueType[] = [
  "Image Mismatch",
  "Attribute Error",
  "Low Resolution",
  "Missing Keywords",
];

const PERIOD_LABELS: Record<string, string> = {
  "7d":  "Last 7 days",
  "30d": "Last 30 days",
  "90d": "Last 90 days",
  "1y":  "Last year",
};

function transformRiskRadar(raw: RiskRadarRaw): TransformedRadar {
  const riskData: Record<string, Record<IssueType, number>> = {};
  for (const cat of raw.data) {
    const row: Record<IssueType, number> = {
      "Image Mismatch":   0,
      "Attribute Error":  0,
      "Low Resolution":   0,
      "Missing Keywords": 0,
    };
    for (const issue of cat.issues) {
      const key = TYPE_MAP[issue.type];
      if (key) row[key] = issue.value;
    }
    riskData[cat.category] = row;
  }
  return {
    categories: raw.data.map((d) => d.category),
    issueTypes: ISSUE_TYPES,
    riskData,
  };
}

// ── Component ──────────────────────────────────────────────────────────────

export function QualityRiskRadar({ dateRange = "30d" }: QualityRiskRadarProps) {
  const [selectedMarketplace, setSelectedMarketplace] = useState<string | null>(null);
  const queryClient = useQueryClient();

  // KEY FIX 1: When dateRange changes, immediately invalidate ALL risk-radar cache
  // entries so React Query ignores any cached data and fetches fresh results.
  // This is needed because staleTime could prevent a refetch even when the key changes
  // if the cached entry was created very recently.
  useEffect(() => {
    queryClient.invalidateQueries({ queryKey: ["executive", "risk-radar"] });
  }, [dateRange, queryClient]);

  const { data: raw, isLoading, isError, error } = useQuery<RiskRadarRaw>({
    // KEY FIX 2: Both dateRange AND selectedMarketplace are in the query key.
    // Any change to either value creates a new cache entry and triggers a fetch.
    queryKey: ["executive", "risk-radar", dateRange, selectedMarketplace],
    queryFn: async () => {
      const params = new URLSearchParams();
      // KEY FIX 3: The backend param is "period" not "dateRange" or "date_range"
      params.set("period", dateRange);
      if (selectedMarketplace) params.set("marketplace", selectedMarketplace);
      const url = `${EXEC_API_BASE}/executive/risk-radar?${params.toString()}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
      return res.json();
    },
    retry: 1,
    // KEY FIX 4: staleTime: 0 means data is immediately considered stale.
    // React Query will always refetch when the component re-renders with a new
    // query key, without waiting for the stale timer to expire.
    staleTime: 0,
    gcTime: 60_000,
  });

  const transformed        = raw ? transformRiskRadar(raw) : null;
  const categories         = transformed?.categories ?? [];
  const issueTypes         = transformed?.issueTypes ?? ISSUE_TYPES;
  const riskData           = transformed?.riskData   ?? {};
  const marketplaceButtons = raw?.marketplaces ?? [];
  const isLive             = !!raw && !isError;

  return (
    <TooltipProvider>
      <div
        className="glass-card rounded-xl p-8 opacity-0 animate-fade-in"
        style={{ animationDelay: "200ms", animationFillMode: "forwards" }}
      >
        {/* ── Header ── */}
        <div className="flex items-start justify-between mb-8">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <h3 className="text-2xl font-bold text-foreground tracking-tight">
                Content Quality Risk Radar
              </h3>
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
              ) : isLive ? (
                <Badge
                  variant="default"
                  className="text-[10px] px-2 py-0.5 bg-success/20 text-success border-success/30 font-medium"
                >
                  Live
                </Badge>
              ) : isError ? (
                <Badge
                  variant="outline"
                  className="text-[10px] px-2 py-0.5 text-destructive border-destructive/30 font-medium"
                >
                  API Error
                </Badge>
              ) : null}
            </div>
            <p className="text-sm text-muted-foreground">
              Issue distribution by category —{" "}
              <span className="font-medium text-foreground">
                {PERIOD_LABELS[dateRange] ?? dateRange}
              </span>
              {selectedMarketplace && (
                <span className="ml-1 font-medium text-foreground">· {selectedMarketplace}</span>
              )}
            </p>
          </div>

          {/* Legend */}
          <div className="flex gap-3 text-xs bg-muted/50 p-2 rounded-lg">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded bg-success" />
              <span className="text-muted-foreground font-medium">Low (&lt;40%)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded bg-warning" />
              <span className="text-muted-foreground font-medium">Medium (40-70%)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded bg-destructive" />
              <span className="text-muted-foreground font-medium">High (&gt;70%)</span>
            </div>
          </div>
        </div>

        {/* ── Error state ── */}
        {isError && (
          <div className="mb-6 p-4 rounded-lg bg-destructive/5 border border-destructive/20 text-sm text-destructive">
            Failed to load data ({String(error)}). Make sure backend is running on{" "}
            <code className="font-mono">{EXEC_API_BASE}</code>.
          </div>
        )}

        {/* ── Skeleton while loading ── */}
        {isLoading && (
          <div className="space-y-6">
            {Array.from({ length: 5 }).map((_, rowIdx) => (
              <div key={rowIdx} className="space-y-2">
                <div className="h-4 w-24 bg-muted rounded animate-pulse" />
                <div className="grid grid-cols-4 gap-3">
                  {Array.from({ length: 4 }).map((_, colIdx) => (
                    <div key={colIdx} className="h-16 rounded-lg bg-muted animate-pulse" />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ── Category rows ── */}
        {!isLoading && categories.length > 0 && (
          <div className="space-y-6">
            {categories.map((category) => {
              const catValues = Object.values(riskData[category] || {});
              const avg =
                catValues.length > 0
                  ? (catValues.reduce((s, v) => s + v, 0) / catValues.length).toFixed(2)
                  : "0";

              return (
                <div key={category} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-base font-semibold text-foreground">{category}</h4>
                    <span className="text-xs text-muted-foreground">{avg}% avg</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    {issueTypes.map((type) => {
                      const value     = riskData[category]?.[type] ?? 0;
                      const intensity = getRiskIntensity(value);
                      return (
                        <Tooltip key={type}>
                          <TooltipTrigger asChild>
                            <div
                              className={cn(
                                "heat-cell p-4 border border-border/50 rounded-xl",
                                "hover:border-opacity-100 transition-all cursor-pointer",
                                intensity === "high"   && "bg-destructive/5 border-destructive/20",
                                intensity === "medium" && "bg-warning/5 border-warning/20",
                                intensity === "low"    && "bg-success/5 border-success/20",
                              )}
                              role="button"
                              tabIndex={0}
                              aria-label={`${category} - ${type}: ${value}%`}
                            >
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-medium text-muted-foreground truncate pr-2">
                                  {type}
                                </span>
                                <span className={cn("text-sm font-bold tabular-nums", getRiskColor(value))}>
                                  {value}%
                                </span>
                              </div>
                              <div className="progress-bar">
                                <div
                                  className={cn("progress-fill", getRiskBg(value))}
                                  style={{ width: `${value}%` }}
                                  aria-valuenow={value}
                                  aria-valuemin={0}
                                  aria-valuemax={100}
                                  role="progressbar"
                                />
                              </div>
                            </div>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p className="font-medium">{category} — {type}</p>
                            <p className="text-xs text-muted-foreground mt-1">
                              Risk Level: {intensity.toUpperCase()} ({value}%)
                            </p>
                          </TooltipContent>
                        </Tooltip>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* ── Empty state ── */}
        {!isLoading && !isError && categories.length === 0 && (
          <div className="text-center py-12 text-sm text-muted-foreground">
            No data available for the selected filters.
          </div>
        )}

        {/* ── Marketplace filter buttons ── */}
        <div className="mt-6 pt-6 border-t border-border/50">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <span className="text-sm font-medium text-muted-foreground">Filter by Marketplace</span>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => {
                  setSelectedMarketplace(null);
                  toast({ title: "Marketplace filter cleared", description: "Showing all marketplaces" });
                }}
                className={cn(
                  "px-4 py-2 text-xs font-semibold rounded-lg transition-all hover:scale-105 active:scale-95",
                  selectedMarketplace === null
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "bg-muted text-muted-foreground hover:bg-muted/80",
                )}
              >
                All
              </button>

              {marketplaceButtons.map((mp) => (
                <button
                  key={mp}
                  onClick={() => {
                    setSelectedMarketplace(mp);
                    toast({ title: "Marketplace changed", description: `Viewing data for ${mp}` });
                  }}
                  className={cn(
                    "px-4 py-2 text-xs font-semibold rounded-lg transition-all hover:scale-105 active:scale-95",
                    selectedMarketplace === mp
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "bg-muted text-muted-foreground hover:bg-muted/80",
                  )}
                  aria-pressed={selectedMarketplace === mp}
                >
                  {mp}
                </button>
              ))}

              {marketplaceButtons.length === 0 && isLoading &&
                ["Amazon.in", "Flipkart", "Takealot"].map((mp) => (
                  <div key={mp} className="h-8 w-20 bg-muted rounded-lg animate-pulse" />
                ))}
            </div>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}