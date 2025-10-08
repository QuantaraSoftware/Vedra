# Config settings for Quantara Web Editor

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
MAX_VIDEO_LENGTH = 600  # seconds (10 minutes)
WATERMARK_TEXT = "Quantara"

FILTERS = {
    "None": lambda clip: clip,
    "Grayscale": lambda clip: clip.fx("blackwhite"),
    "Sepia": lambda clip: clip.fx("colorx", 1.5).fx("lum_contrast", lum=0, contrast=30),
    "Invert": lambda clip: clip.fx("invert_colors"),
    "Brighten": lambda clip: clip.fx("colorx", 1.3),
}

AI_FEATURES = [
    "Auto-caption: To be integrated with Whisper/Faster-Whisper",
    "Background Removal: To be integrated with rembg or U2Net",
    "Style Transfer: To be integrated with Torch style models"
]
