/**
 * Centralized API Configuration
 * All API base URLs are defined here and imported by other modules
 */

/**
 * Image-to-Text API
 * Used by: ImageToText page, image-to-text-api.ts
 */
export const IMAGE_TO_TEXT_API_URL = 
  import.meta.env.VITE_IMAGE_TO_TEXT_API_URL ?? 
  "https://e-commerce-1-imageto-txt.onrender.com";

/**
 * Color Mismatch API (also used for Image Description)
 * Used by: ColorMismatch page, color-mismatch-api.ts
 */
export const COLOR_MISMATCH_API_URL = 
  import.meta.env.VITE_MISMATCH_API_URL ?? 
  "http://localhost:8000";

/**
 * Executive Dashboard API
 * Used by: Dashboard page, PhotoshootPerformance component, QualityRiskRadar component
 */
export const EXECUTIVE_API_URL = 
  import.meta.env.VITE_EXECUTIVE_API_URL ?? 
  import.meta.env.VITE_MISMATCH_API_URL ?? 
  "http://localhost:8000";

/**
 * AI Photoshoot API
 * Used by: AIPhotoshoot page
 */
export const PHOTOSHOOT_API_URL = 
  import.meta.env.VITE_PHOTOSHOOT_API_URL ?? 
  "https://ai-photoshoot-f9qy.onrender.com";

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
