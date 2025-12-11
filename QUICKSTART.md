# QUICK REFERENCE GUIDE

## Installation (One-Time Setup)

### Linux/macOS
```bash
# Install Tesseract (required for OCR)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Install Python dependencies
pip3 install -r requirements.txt

# Run the application
python3 main.py
```

### Windows
```batch
# Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Or run the setup script
setup.bat

# Run the application
python main.py
```

## Running the Application

```bash
# From the project directory
python3 main.py
```

## GUI Operations Cheat Sheet

| Action | Steps |
|--------|-------|
| **Load Image** | Click "Load Image (JPG/PNG)" → Select file |
| **Open Camera** | Click "Open Live Camera" (shows live feed) |
| **Select ROI** | Click and drag on image to draw rectangle |
| **Clear ROI** | Click "Clear ROI Selection" |
| **OCR Full Image** | Click "OCR Full Image" → View text in panel |
| **OCR ROI Only** | Draw rectangle → Click "OCR Selected ROI" |
| **Show Text Boxes** | Click "Show Text Box Overlay" |
| **Change Preprocessing** | Select mode from dropdown → Click OCR button |
| **Adjust Threshold** | Use spinbox (0-255) → Apply changes |

## Keyboard Shortcuts
- None implemented (use mouse for all operations)

## Preprocessing Modes

| Mode | Best For | Speed |
|------|----------|-------|
| **Grayscale** | Most images | Fast |
| **Threshold** | High contrast documents | Fast |
| **Adaptive Threshold** | Variable lighting | Medium |
| **Morphological** | Noisy images | Slow |

## Expected Performance

- **Image Load**: Instant
- **Full Image OCR**: 2-5 seconds
- **ROI OCR**: 1-2 seconds
- **Camera Start**: 1 second
- **Frame Rate**: ~30 FPS

## Troubleshooting

### Camera Won't Open
```bash
# Check if camera is detected
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"

# Linux: May need to add user to video group
sudo usermod -a -G video $USER
# Then logout and login again
```

### OCR Returns Empty
1. Try "Adaptive Threshold" mode
2. Adjust threshold value (try 80-150)
3. Ensure image has clear, dark text
4. Check image resolution is reasonable

### Application Won't Start
```bash
# Verify Python version
python3 --version  # Must be 3.8+

# Verify dependencies
pip3 list | grep -E "PyQt5|opencv|pytesseract"

# Verify Tesseract
tesseract --version
```

## Project Files Overview

| File | Purpose | Lines |
|------|---------|-------|
| main.py | Main GUI application | 414 |
| ocr_utils.py | OCR and preprocessing | 149 |
| camera_utils.py | Camera handling | 173 |
| README.md | Full documentation | - |
| requirements.txt | Dependencies | - |

## Key Classes

### main.py
- `TextScannerApp`: Main window (QMainWindow)
- `ImageCanvas`: Image display and ROI selection (QLabel)
- `CameraThread`: Background camera capture (QThread)

### camera_utils.py
- `CameraCapture`: OpenCV wrapper with resolution/FPS control

## Key Functions

### ocr_utils.py
- `preprocess_image()`: Apply preprocessing filters
- `extract_text_with_boxes()`: Run OCR extraction
- `get_text_boxes()`: Get bounding box coordinates
- `extract_text_from_roi()`: Process specific region

## Dependencies

All dependencies specified in `requirements.txt`:
- PyQt5 (GUI framework)
- opencv-python (camera and image processing)
- pytesseract (OCR engine wrapper)
- Pillow (image handling)
- numpy (numerical operations)

Tesseract OCR engine must be installed separately on your system.

## Common Issues & Solutions

### ImportError: No module named PyQt5
```bash
pip3 install PyQt5
```

### ImportError: No module named cv2
```bash
pip3 install opencv-python
```

### ImportError: No module named pytesseract
```bash
pip3 install pytesseract
```

### tesseract is not installed or it's not in your PATH
- Tesseract OCR engine not installed (see Installation section)
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

### QXcbConnection: Could not connect to display (Linux)
- Running on headless system without display
- Use SSH with X11 forwarding: `ssh -X user@host`

### Camera frame is black/empty
- Camera permission issue (Linux)
- Wrong camera index (try VideoCapture(1) instead of 0)
- Camera already in use by another application

## Tips for Best Results

1. **Good Lighting**: Ensure document is well-lit
2. **Clear Text**: Use high-contrast images
3. **Straight Angle**: Capture documents straight on, not at angles
4. **High Resolution**: Larger images give better OCR results
5. **Try Modes**: Experiment with different preprocessing modes
6. **ROI Selection**: Select text regions for faster, more accurate processing

## Performance Tuning

### Faster OCR
- Use smaller images or ROI selection
- Use "Grayscale" mode instead of adaptive
- Reduce image resolution before processing

### Better Accuracy
- Use "Adaptive Threshold" mode
- Adjust threshold value (80-150 usually best)
- Ensure good image quality
- Use full preprocessing steps

## Development Notes

- All code is Python 3.8+ compatible
- Cross-platform (Linux, Windows, macOS)
- No external C++ libraries required (beyond Tesseract)
- Modular design allows easy extensions
- Thread-safe camera handling with PyQt5

---

For complete documentation, see **README.md**
