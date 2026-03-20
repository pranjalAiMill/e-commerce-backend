/**
 * AI Photoshoot API Service
 * 
 * This service layer integrates with the ai-photoshoot-proto-main backend.
 * Endpoints are defined in ai-photoshoot-proto-main/backend/main.py
 * 
 * Base URL: Configured via VITE_PHOTOSHOOT_API_URL environment variable
 * Default: https://ai-photoshoot-f9qy.onrender.com (production)
 * Fallback: http://localhost:8002 (local development)
 */

const PHOTOSHOOT_BASE_URL = import.meta.env.VITE_PHOTOSHOOT_API_URL ?? "http://localhost:8000";

// ==================================================
// TYPE DEFINITIONS
// ==================================================

export interface PhotoshootTemplate {
  id: string;
  name: string;
  uses: string;
  img: string;
  prompt: string;
}

export interface PhotoshootTemplatesResponse {
  Indian: PhotoshootTemplate[];
  "South African": PhotoshootTemplate[];
  Global: PhotoshootTemplate[];
}

export interface GeneratePhotoshootRequest {
  template_id: string;
  region: string;
  skin_tone: string;
  cloth_image: File;
}

export interface GeneratedImageView {
  view: "Front" | "Side" | "Angle";
  image: string; // base64 encoded image
}

export interface GeneratePhotoshootResponse {
  status: "success" | "error";
  images: GeneratedImageView[];
  error?: string;
}

// ==================================================
// ERROR HANDLING
// ==================================================

export class PhotoshootApiError extends Error {
  status: number;
  detail?: string;

  constructor(message: string, status: number, detail?: string) {
    super(message);
    this.name = "PhotoshootApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function handlePhotoshootResponse<T>(res: Response): Promise<T> {
  const contentType = res.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");

  if (!res.ok) {
    let errorMessage = `Request failed with status ${res.status}`;
    let errorDetail: string | undefined;

    if (isJson) {
      try {
        const body = await res.json();
        errorMessage = body?.detail || body?.error || body?.message || errorMessage;
        errorDetail = body?.detail;
      } catch {
        // Ignore parse error, use default message
      }
    }

    throw new PhotoshootApiError(errorMessage, res.status, errorDetail);
  }

  if (!isJson) {
    return res as unknown as T;
  }

  return (await res.json()) as T;
}

// ==================================================
// API FUNCTIONS
// ==================================================

/**
 * Fetch all photoshoot templates organized by region
 */
export async function getPhotoshootTemplates(): Promise<PhotoshootTemplatesResponse> {
  const url = `${PHOTOSHOOT_BASE_URL}/templates`;
  const res = await fetch(url);
  return handlePhotoshootResponse<PhotoshootTemplatesResponse>(res);
}

/**
 * Generate photoshoot with 3 views (Front, Side, Angle)
 * @param params - Generation parameters including template, region, skin tone, and image
 * @returns Response with base64-encoded images for each view
 */
export async function generatePhotoshoot(
  params: GeneratePhotoshootRequest
): Promise<GeneratePhotoshootResponse> {
  const url = `${PHOTOSHOOT_BASE_URL}/generate-photoshoot`;
  
  const formData = new FormData();
  formData.append("template_id", params.template_id);
  formData.append("region", params.region);
  formData.append("skin_tone", params.skin_tone);
  formData.append("cloth_image", params.cloth_image);

  const res = await fetch(url, {
    method: "POST",
    body: formData,
  });

  return handlePhotoshootResponse<GeneratePhotoshootResponse>(res);
}

/**
 * Convert base64 string to blob URL for display
 */
export function base64ToBlobUrl(base64: string, mimeType: string = "image/png"): string | null {
  try {
    // Remove data URL prefix if present
    const base64Data = base64.replace(/^data:image\/\w+;base64,/, "");
    const binaryString = atob(base64Data);
    const bytes = new Uint8Array(binaryString.length);
    
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    
    const blob = new Blob([bytes], { type: mimeType });
    return URL.createObjectURL(blob);
  } catch (error) {
    console.error("Error converting base64 to blob URL:", error);
    return null;
  }
}
