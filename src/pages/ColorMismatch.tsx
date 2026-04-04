import { useState, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  Palette,
  Upload,
  Loader2,
  CheckCircle,
  AlertCircle,
  Sparkles,
  Info,
  X,
  FileText,
  Zap,
  TrendingUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";
import {
  detectColor,
  detectAndMatch,
  type ColorDetectionResult,
  type DetectAndMatchResult,
} from "@/lib/color-mismatch-api";

interface ImageDescription {
  title: string;
  short_description: string;
  long_description: string;
  bullet_points: string[];
  attributes: Record<string, string>;
}

export default function ColorMismatch() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [expectedColor, setExpectedColor] = useState("");
  const [detectionResult, setDetectionResult] = useState<ColorDetectionResult | null>(null);
  const [matchResult, setMatchResult] = useState<DetectAndMatchResult | null>(null);
  const [imageDescription, setImageDescription] = useState<ImageDescription | null>(null);
  const [isGeneratingDescription, setIsGeneratingDescription] = useState(false);

  // Detect color mutation
  const detectMutation = useMutation({
    mutationFn: (file: File) => detectColor(file),
    onSuccess: (data) => {
      setDetectionResult(data);
      toast({
        title: "Color Detected",
        description: `Detected: ${data.detected_color}`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Detection Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Detect and match mutation
  const detectAndMatchMutation = useMutation({
    mutationFn: ({ file, expectedColor }: { file: File; expectedColor: string }) =>
      detectAndMatch(file, expectedColor),
    onSuccess: (data) => {
      setMatchResult(data);
      setDetectionResult(data.detection);
      toast({
        title: "Analysis Complete",
        description: `Verdict: ${data.verdict}`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Analysis Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        toast({
          title: "Invalid file type",
          description: "Please select an image file (JPEG, PNG, etc.)",
          variant: "destructive",
        });
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        toast({
          title: "File too large",
          description: "Please select an image smaller than 10MB",
          variant: "destructive",
        });
        return;
      }

      setUploadedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setUploadedImage(null);
    setImagePreview(null);
    setDetectionResult(null);
    setMatchResult(null);
    setImageDescription(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleDetectColor = () => {
    if (!uploadedImage) {
      toast({
        title: "No image",
        description: "Please upload an image first",
        variant: "destructive",
      });
      return;
    }
    detectMutation.mutate(uploadedImage);
  };

  const handleDetectAndMatch = () => {
    if (!uploadedImage) {
      toast({
        title: "No image",
        description: "Please upload an image first",
        variant: "destructive",
      });
      return;
    }
    if (!expectedColor.trim()) {
      toast({
        title: "Expected color required",
        description: "Please enter the expected/catalog color",
        variant: "destructive",
      });
      return;
    }
    detectAndMatchMutation.mutate({ file: uploadedImage, expectedColor: expectedColor.trim() });
  };

  const handleGenerateDescription = async () => {
    if (!uploadedImage) {
      toast({
        title: "No image",
        description: "Please upload an image first",
        variant: "destructive",
      });
      return;
    }

    setIsGeneratingDescription(true);
    setImageDescription(null);

    try {
      const formData = new FormData();
      formData.append("image", uploadedImage);
      formData.append("language", "en");

      const baseUrl = import.meta.env.VITE_MISMATCH_API_URL || "https://e-commerce-dashboard-asapc3eac9b9dfb7.westus2-01.azurewebsites.net";
      const response = await fetch(`${baseUrl}/generate-description`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Failed to generate description: ${response.statusText}`);
      }

      const data = await response.json();
      setImageDescription(data);
      toast({
        title: "Description Generated",
        description: "AI-powered product description created successfully",
      });
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: error instanceof Error ? error.message : "Failed to generate description",
        variant: "destructive",
      });
    } finally {
      setIsGeneratingDescription(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <div className="p-4 lg:p-8 space-y-8 max-w-[1920px] mx-auto">
        {/* Enhanced Header */}
        <div className="space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-gradient-to-br from-ai/10 to-ai/5 border border-ai/20">
                  <Palette className="w-6 h-6 text-ai" />
                </div>
                <div>
                  <h1 className="text-3xl lg:text-4xl font-bold text-foreground tracking-tight">
                    Color Mismatch Detection
                  </h1>
                  <p className="text-sm text-muted-foreground mt-1">
                    AI-powered color detection, matching, and product description generation
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge className="bg-gradient-to-w from-ai/10 to-ai/5 text-ai border-ai/20 px-3 py-1.5">
                <Sparkles className="w-3.5 h-3.5 mr-1.5" />
                AI Powered
              </Badge>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Enhanced Left Sidebar - Controls */}
          <div className="lg:col-span-1 space-y-4">
            <Card className="p-6 lg:p-8 border border-border/40 bg-gradient-to-br from-card via-card/95 to-card/90 backdrop-blur-sm shadow-xl shadow-primary/5">
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border/30">
                <div className="p-2.5 rounded-xl bg-gradient-to-br from-ai/20 to-ai/10 border border-ai/20">
                  <Upload className="w-5 h-5 text-ai" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground text-lg">Upload & Test</h3>
                  <p className="text-xs text-muted-foreground">Upload an image to analyze</p>
                </div>
              </div>
              
              <div className="space-y-5">
                <div className="space-y-3">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                    id="image-upload"
                  />
                  
                  {!imagePreview ? (
                    <div
                      className="w-full aspect-video bg-gradient-to-br from-muted/30 via-muted/20 to-muted/30 rounded-2xl flex items-center justify-center border-2 border-dashed border-border/40 cursor-pointer hover:border-ai/40 hover:bg-ai/5 hover:shadow-lg transition-all duration-300 group"
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <div className="text-center p-8">
                        <div className="inline-flex p-4 rounded-2xl bg-ai/10 mb-4 group-hover:bg-ai/20 transition-colors">
                          <Upload className="w-8 h-8 text-ai" />
                        </div>
                        <p className="text-sm font-medium text-foreground mb-1">Upload Product Image</p>
                        <p className="text-xs text-muted-foreground">Click or drag and drop</p>
                      </div>
                    </div>
                  ) : (
                    <div className="relative group">
                      <div className="relative rounded-2xl overflow-hidden border-2 border-border/40 shadow-lg">
                        <img
                          src={imagePreview}
                          alt="Preview"
                          className="w-full aspect-video object-cover"
                        />
                        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                          <Button
                            variant="destructive"
                            size="icon"
                            className="opacity-0 group-hover:opacity-100 transition-opacity h-10 w-10"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleRemoveImage();
                            }}
                          >
                            <X className="w-5 h-5" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-3 pt-2 border-t border-border/30">
                  <label className="text-sm font-semibold text-foreground flex items-center gap-2">
                    <Palette className="w-4 h-4 text-muted-foreground" />
                    Expected Color
                  </label>
                  <Input
                    placeholder="e.g., blue, red, navy blue"
                    value={expectedColor}
                    onChange={(e) => setExpectedColor(e.target.value)}
                    className="h-11 border-border/40 focus:border-ai/40"
                  />
                  <div className="flex items-start gap-2 p-3 bg-muted/30 rounded-lg text-xs text-muted-foreground border border-border/20">
                    <Info className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                    <span>Enter the catalog/expected color for comparison</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 pt-2">
                  <Button
                    size="lg"
                    onClick={handleDetectColor}
                    disabled={detectMutation.isPending || !uploadedImage}
                    className="w-full bg-ai hover:bg-ai/90"
                  >
                    {detectMutation.isPending ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Detecting...
                      </>
                    ) : (
                      <>
                        <Palette className="w-4 h-4 mr-2" />
                        Detect
                      </>
                    )}
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={handleDetectAndMatch}
                    disabled={detectAndMatchMutation.isPending || !uploadedImage || !expectedColor.trim()}
                    className="w-full border-2"
                  >
                    {detectAndMatchMutation.isPending ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Match
                      </>
                    )}
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={handleGenerateDescription}
                    disabled={isGeneratingDescription || !uploadedImage}
                    className="w-full border-2 border-primary/30 hover:bg-primary/10"
                  >
                    {isGeneratingDescription ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="w-4 h-4 mr-2" />
                        Describe
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </Card>
          </div>

          {/* Enhanced Main Results Area */}
          <div className="lg:col-span-2 space-y-4">
            {/* Image Description Results */}
            {imageDescription && (
              <Card className="p-6 lg:p-8 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-primary/10 backdrop-blur-sm shadow-lg">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-primary/20">
                    <FileText className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">AI-Generated Product Description</h3>
                </div>
                <div className="space-y-4">
                  {imageDescription.title && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Title</div>
                      <div className="text-xl font-bold text-foreground">{imageDescription.title}</div>
                    </div>
                  )}
                  
                  {imageDescription.short_description && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Short Description</div>
                      <div className="text-sm text-foreground leading-relaxed">{imageDescription.short_description}</div>
                    </div>
                  )}

                  {imageDescription.long_description && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Detailed Description</div>
                      <div className="text-sm text-foreground leading-relaxed">{imageDescription.long_description}</div>
                    </div>
                  )}

                  {imageDescription.bullet_points && imageDescription.bullet_points.length > 0 && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Key Features</div>
                      <ul className="space-y-2">
                        {imageDescription.bullet_points.map((point, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-foreground">
                            <CheckCircle className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                            <span>{point}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {imageDescription.attributes && Object.keys(imageDescription.attributes).length > 0 && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Attributes</div>
                      <div className="grid grid-cols-2 gap-3">
                        {Object.entries(imageDescription.attributes).map(([key, value]) => (
                          <div key={key} className="p-3 rounded-lg bg-background/50 border border-border/30">
                            <div className="text-xs text-muted-foreground mb-1">{key}</div>
                            <div className="text-sm font-medium text-foreground">{value}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {/* Enhanced Detection Results */}
            {detectionResult && (
              <Card className="p-6 lg:p-8 border-2 border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-ai/10">
                    <Palette className="w-5 h-5 text-ai" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">Detection Results</h3>
                </div>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-lg bg-gradient-to-br from-ai/10 to-ai/5 border border-ai/20">
                      <div className="text-xs font-medium text-muted-foreground mb-1">Detected Color</div>
                      <div className="text-2xl font-bold text-foreground">{detectionResult.detected_color}</div>
                    </div>
                    {detectionResult.detected_confidence !== null && (
                      <div className="p-4 rounded-lg bg-gradient-to-br from-muted/50 to-muted/30 border border-border/50">
                        <div className="text-xs font-medium text-muted-foreground mb-1">Confidence</div>
                        <div className="text-2xl font-bold text-foreground">
                          {(detectionResult.detected_confidence * 100).toFixed(1)}%
                        </div>
                      </div>
                    )}
                  </div>

                  {detectionResult.top_candidates && detectionResult.top_candidates.length > 1 && (
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-muted-foreground">Top Candidates</div>
                      <div className="grid grid-cols-2 gap-2">
                        {detectionResult.top_candidates.slice(0, 4).map(([color, confidence], idx) => (
                          <div key={idx} className="flex items-center justify-between p-3 bg-muted/30 rounded-lg border border-border/30">
                            <span className="text-sm font-medium">{color}</span>
                            {confidence !== null && (
                              <Badge variant="outline" className="text-xs">
                                {(confidence * 100).toFixed(1)}%
                              </Badge>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {/* Enhanced Match Results */}
            {matchResult && (
              <Card className="p-6 lg:p-8 border-2 border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-ai/10">
                    <CheckCircle className="w-5 h-5 text-ai" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">Match Analysis</h3>
                </div>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className={cn(
                      "p-4 rounded-lg border-2",
                      matchResult.verdict === "Match"
                        ? "bg-success/10 border-success/30"
                        : "bg-destructive/10 border-destructive/30"
                    )}>
                      <div className="text-xs font-medium text-muted-foreground mb-2">Expected</div>
                      <div className="text-xl font-bold text-foreground">{matchResult.expected_color}</div>
                    </div>
                    <div className={cn(
                      "p-4 rounded-lg border-2",
                      matchResult.verdict === "Match"
                        ? "bg-success/10 border-success/30"
                        : "bg-destructive/10 border-destructive/30"
                    )}>
                      <div className="text-xs font-medium text-muted-foreground mb-2">Detected</div>
                      <div className="text-xl font-bold text-foreground">{matchResult.detection.detected_color}</div>
                    </div>
                  </div>
                  <div className={cn(
                    "p-5 rounded-lg border-2 flex items-center justify-between",
                    matchResult.verdict === "Match"
                      ? "bg-success/10 border-success/30"
                      : "bg-destructive/10 border-destructive/30"
                  )}>
                    <div>
                      <div className="text-sm font-medium text-muted-foreground mb-1">Final Verdict</div>
                      <div className="text-2xl font-bold text-foreground">{matchResult.verdict}</div>
                    </div>
                    <Badge
                      variant={matchResult.verdict === "Match" ? "default" : "destructive"}
                      className={cn(
                        "text-lg px-4 py-2",
                        matchResult.verdict === "Match"
                          ? "bg-success text-success-foreground"
                          : "bg-destructive text-destructive-foreground"
                      )}
                    >
                      {matchResult.verdict === "Match" ? "✓ Match" : "✗ Mismatch"}
                    </Badge>
                  </div>
                </div>
              </Card>
            )}

            {!detectionResult && !matchResult && !imageDescription && (
              <Card className="p-12 lg:p-16 border-2 border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
                <div className="text-center space-y-6">
                  <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-primary/10 to-primary/5 border-2 border-primary/20 flex items-center justify-center">
                    <Zap className="w-10 h-10 text-primary/60" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-3">Ready to Analyze</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed max-w-md mx-auto">
                      Upload an image and click "Detect" for color detection, "Match" for color comparison, or "Describe" for AI-generated product description
                    </p>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
