import { useState } from "react";
import { ImageIcon, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { getProductImageUrl, getMismatchDatasetImageUrl } from "@/lib/color-mismatch-api";

interface ProductImageProps {
  productId: string | number;
  index?: number;
  alt?: string;
  className?: string;
  fallbackClassName?: string;
  onError?: () => void;
  onLoad?: () => void;
  useMismatchBackend?: boolean; // Use port 8001 for mismatch dataset images
}

export default function ProductImage({
  productId,
  index,
  alt = "Product image",
  className,
  fallbackClassName,
  onError,
  onLoad,
  useMismatchBackend = false,
}: ProductImageProps) {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  const imageUrl = useMismatchBackend 
    ? getMismatchDatasetImageUrl(productId, index)
    : getProductImageUrl(productId, index);

  const handleError = () => {
    setImageError(true);
    setImageLoading(false);
    onError?.();
  };

  const handleLoad = () => {
    setImageLoading(false);
    onLoad?.();
  };

  if (imageError) {
    return (
      <div
        className={cn(
          "flex flex-col items-center justify-center bg-muted/30 rounded-lg border border-border/50",
          fallbackClassName
        )}
      >
        <ImageIcon className="w-8 h-8 text-muted-foreground mb-2" />
        <p className="text-xs text-muted-foreground text-center px-2">Image not found</p>
      </div>
    );
  }

  return (
    <div className={cn("relative", className)}>
      {imageLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-muted/30 rounded-lg">
          <div className="animate-pulse text-xs text-muted-foreground">Loading...</div>
        </div>
      )}
      <img
        src={imageUrl}
        alt={alt}
        onError={handleError}
        onLoad={handleLoad}
        className={cn(
          "w-full h-full object-cover rounded-lg border border-border/50",
          imageLoading && "opacity-0"
        )}
      />
    </div>
  );
}
