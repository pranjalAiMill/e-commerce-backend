/**
 * Centralized API Configuration
 * All API base URLs are defined here and imported by other modules
 */

/**
 * Image-to-Text API
 * Used by: ImageToText page, image-to-text-api.ts
 */
export const IMAGE_TO_TEXT_API_URL = 
  "http://localhost:8000";

/**
 * Color Mismatch API (also used for Image Description)
 * Used by: ColorMismatch page, color-mismatch-api.ts
 */
export const COLOR_MISMATCH_API_URL = 
  "http://localhost:8000";

/**
 * Executive Dashboard API
 * Used by: Dashboard page, PhotoshootPerformance component, QualityRiskRadar component
 */
export const EXECUTIVE_API_URL = 
  "http://localhost:8001";

/**
 * AI Photoshoot API
 * Used by: AIPhotoshoot page
 */
export const PHOTOSHOOT_API_URL = 
  import.meta.env.VITE_PHOTOSHOOT_API_URL ?? 
  "http://localhost:8000";

/**
 * Helper function to ensure URL doesn't have trailing slash
 */
export function normalizeUrl(url: string): string {
  return url.replace(/\/$/, '');
}

/**
 * Helper function to build full API endpoint URL
 */
export function buildApiUrl(baseUrl: string, endpoint: string): string {
  const normalized = normalizeUrl(baseUrl);
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${normalized}${cleanEndpoint}`;
}
