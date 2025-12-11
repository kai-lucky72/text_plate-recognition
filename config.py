#!/usr/bin/env python3
"""
Configuration and Advanced Settings for Printed Text Scanner
Can be imported and customized for different deployment scenarios
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================
CAMERA_CONFIG = {
    "camera_index": 0,           # Primary camera (0 for default, 1 for secondary, etc.)
    "frame_width": 640,          # Frame width in pixels
    "frame_height": 480,         # Frame height in pixels
    "fps": 30,                   # Target frames per second
    "auto_focus": True,          # Enable camera autofocus if available
    "brightness": -1,            # -1 = auto, or set value 0-100
    "contrast": -1,              # -1 = auto, or set value 0-100
}

# ============================================================================
# OCR PREPROCESSING SETTINGS
# ============================================================================
OCR_CONFIG = {
    "default_mode": "Grayscale",        # Default preprocessing mode
    "default_threshold": 127,            # Default threshold value (0-255)
    "noise_filter_kernel": 5,            # Median blur kernel size (odd number)
    "morphology_iterations": 1,          # Morph operations iterations
    "adaptive_threshold_block_size": 11, # Must be odd
}

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
DISPLAY_CONFIG = {
    "window_width": 1200,               # Default window width
    "window_height": 800,               # Default window height
    "canvas_min_width": 400,            # Minimum canvas width
    "canvas_min_height": 400,           # Minimum canvas height
    "text_display_height": 200,         # Minimum text display height
    "roi_color_rgb": (0, 255, 0),      # ROI outline color (G, B, R for OpenCV)
    "roi_thickness": 2,                 # ROI rectangle line thickness
    "text_box_color_rgb": (0, 255, 0), # Text box outline color
    "text_box_thickness": 2,            # Text box line thickness
    "font_size": 10,                    # Text font size
}

# ============================================================================
# FILE SETTINGS
# ============================================================================
FILE_CONFIG = {
    "supported_image_formats": ["jpg", "jpeg", "png", "bmp", "tiff"],
    "max_image_dimension": 4096,        # Maximum width or height in pixels
    "quality_jpeg": 95,                 # JPEG save quality (1-100)
}

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================
PERFORMANCE_CONFIG = {
    "camera_thread_enabled": True,      # Use threaded camera capture
    "cache_processed_images": False,    # Cache last processed image
    "memory_limit_mb": 500,             # Approximate memory limit
}

# ============================================================================
# TESSERACT SETTINGS (Advanced)
# ============================================================================
TESSERACT_CONFIG = {
    # Optional: Path to tesseract if not in system PATH
    # "exe_path": "/usr/bin/tesseract",  # Linux/macOS
    # "exe_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # Windows
    
    # Tesseract language config
    "lang": "eng",                      # Language: eng=English, others available
    "psm": 3,                           # Page segmentation mode (0-13)
    # 0=orientation and script detection
    # 1=automatic page segmentation with osd
    # 3=fully automatic page segmentation (default)
    # 6=assume single column of text
    # 7=treat image as single text line
    "oem": 3,                           # OCR engine mode (0-3)
    # 0=legacy engine only
    # 1=neural nets LSTM only
    # 2=legacy + LSTM
    # 3=default (auto-select)
}

# ============================================================================
# LOGGING SETTINGS
# ============================================================================
LOGGING_CONFIG = {
    "enable_logging": True,
    "log_file": "text_scanner.log",
    "log_level": "INFO",               # DEBUG, INFO, WARNING, ERROR
    "log_to_console": True,
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================
FEATURES = {
    "enable_camera": True,              # Show camera features
    "enable_roi_selection": True,       # Show ROI selection
    "enable_overlay": True,             # Show text box overlay
    "enable_preprocessing_modes": True, # Show preprocessing options
    "enable_threshold_control": True,   # Show threshold spinbox
    "enable_status_bar": True,          # Show status messages
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_camera_config():
    """Get camera configuration dict."""
    return CAMERA_CONFIG.copy()


def get_ocr_config():
    """Get OCR configuration dict."""
    return OCR_CONFIG.copy()


def get_tesseract_path():
    """
    Get the tesseract executable path.
    Returns None if using system PATH.
    """
    import sys
    
    # Try to get from config first
    if "exe_path" in TESSERACT_CONFIG:
        return TESSERACT_CONFIG["exe_path"]
    
    # Try to detect automatically
    try:
        import shutil
        path = shutil.which("tesseract")
        return path
    except:
        return None


def validate_camera_settings():
    """Validate camera settings are reasonable."""
    cfg = CAMERA_CONFIG
    assert 0 <= cfg["camera_index"] <= 10, "Invalid camera index"
    assert 320 <= cfg["frame_width"] <= 4096, "Invalid frame width"
    assert 240 <= cfg["frame_height"] <= 4096, "Invalid frame height"
    assert 10 <= cfg["fps"] <= 120, "Invalid FPS"
    return True


def validate_ocr_settings():
    """Validate OCR settings are reasonable."""
    cfg = OCR_CONFIG
    assert cfg["default_mode"] in [
        "Grayscale", "Threshold", "Adaptive Threshold", "Morphological"
    ], "Invalid preprocessing mode"
    assert 0 <= cfg["default_threshold"] <= 255, "Invalid threshold"
    return True


# ============================================================================
# ADVANCED: CUSTOM TESSERACT OPTIONS
# ============================================================================

def get_tesseract_config_string():
    """
    Generate tesseract configuration string for advanced users.
    Format: --psm N --oem M -l lang config_params
    """
    cfg = TESSERACT_CONFIG
    config_str = f'--psm {cfg["psm"]} --oem {cfg["oem"]} -l {cfg["lang"]}'
    return config_str


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Printed Text Scanner - Configuration Module")
    print("=" * 60)
    print()
    
    print("Camera Configuration:")
    for key, value in CAMERA_CONFIG.items():
        print(f"  {key}: {value}")
    
    print()
    print("OCR Configuration:")
    for key, value in OCR_CONFIG.items():
        print(f"  {key}: {value}")
    
    print()
    print("Tesseract Configuration:")
    for key, value in TESSERACT_CONFIG.items():
        print(f"  {key}: {value}")
    
    print()
    print("Validation Results:")
    try:
        validate_camera_settings()
        print("  ✓ Camera settings valid")
    except AssertionError as e:
        print(f"  ✗ Camera settings invalid: {e}")
    
    try:
        validate_ocr_settings()
        print("  ✓ OCR settings valid")
    except AssertionError as e:
        print(f"  ✗ OCR settings invalid: {e}")
    
    print()
    print("Tesseract Config String:")
    print(f"  {get_tesseract_config_string()}")
