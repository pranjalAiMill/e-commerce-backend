/**
 * Centralized API Configuration
 * All API base URLs are defined here and imported by other modules
 */

/**
 * Image-to-Text API
 * Used by: ImageToText page, image-to-text-api.ts
 * Backend: unified_main.py (port 8000)
 */
export const IMAGE_TO_TEXT_API_URL = 
  import.meta.env.VITE_IMAGE_TO_TEXT_API_URL ?? 
  "http://localhost:8000";

/**
 * Color Mismatch API (also used for Image Description)
 * Used by: ColorMismatch page, color-mismatch-api.ts
 * Backend: unified_main.py (port 8000)
 */
export const COLOR_MISMATCH_API_URL = 
  import.meta.env.VITE_MISMATCH_API_URL ?? 
  "http://localhost:8000";

/**
 * Executive Dashboard & Mismatch Engine API
 * Used by: Dashboard page, MismatchEngine page, PhotoshootPerformance, QualityRiskRadar
 * Backend: mismatch_backend.py (port 8001)
 */
export const EXECUTIVE_API_URL = 
  import.meta.env.VITE_EXECUTIVE_API_URL ?? 
  "http://localhost:8001";

/**
 * AI Photoshoot API
 * Used by: AIPhotoshoot page
 * Backend: unified_main.py (port 8000) or external service
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
