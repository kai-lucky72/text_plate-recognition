#!/usr/bin/env python3
"""
OCR Utilities - Text extraction and preprocessing functions.
Handles image preprocessing and pytesseract-based OCR operations.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image, mode="Grayscale", threshold=127):
    """
    Preprocess image for OCR.
    
    Args:
        image: Input image (BGR format from OpenCV)
        mode: Preprocessing mode ("Grayscale", "Threshold", "Adaptive Threshold", "Morphological")
        threshold: Threshold value for binary conversion (0-255)
    
    Returns:
        Processed image ready for OCR
    """
    if image is None or image.size == 0:
        return image
    
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Apply denoising
    denoised = cv2.medianBlur(gray, 5)
    
    if mode == "Grayscale":
        return denoised
    
    elif mode == "Threshold":
        # Simple binary threshold
        _, binary = cv2.threshold(denoised, threshold, 255, cv2.THRESH_BINARY)
        return binary
    
    elif mode == "Adaptive Threshold":
        # Adaptive threshold for varying lighting
        adaptive = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return adaptive
    
    elif mode == "Morphological":
        # Binary + morphological operations for noise removal
        _, binary = cv2.threshold(denoised, threshold, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=1)
        return morph
    
    return denoised


def extract_text_with_boxes(image):
    """
    Extract text from image using pytesseract.
    
    Args:
        image: Preprocessed image (grayscale or binary)
    
    Returns:
        Extracted text as string
    """
    if image is None or image.size == 0:
        return ""
    
    try:
        # Convert to PIL Image for pytesseract
        pil_image = Image.fromarray(image)
        
        # Run OCR with Tesseract
        text = pytesseract.image_to_string(pil_image)
        
        return text.strip() if text else ""
    
    except Exception as e:
        print(f"Error during OCR: {e}")
        return f"Error: {str(e)}"


def get_text_boxes(image):
    """
    Get bounding boxes for detected text blocks.
    
    Args:
        image: Preprocessed image (grayscale or binary)
    
    Returns:
        List of tuples (x, y, width, height, confidence)
    """
    if image is None or image.size == 0:
        return []
    
    try:
        pil_image = Image.fromarray(image)
        
        # Get detailed text data including bounding boxes
        data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
        
        boxes = []
        for i in range(len(data['text'])):
            # Filter out empty detections
            if int(data['conf'][i]) > 0:
                x = int(data['left'][i])
                y = int(data['top'][i])
                w = int(data['width'][i])
                h = int(data['height'][i])
                conf = int(data['conf'][i])
                
                boxes.append((x, y, w, h, conf))
        
        return boxes
    
    except Exception as e:
        print(f"Error getting text boxes: {e}")
        return []


def extract_text_from_roi(image, roi_coords, preprocess_mode="Grayscale", threshold=127):
    """
    Extract text from a specific ROI.
    
    Args:
        image: Input image
        roi_coords: Tuple of (x, y, width, height)
        preprocess_mode: Preprocessing mode
        threshold: Threshold value
    
    Returns:
        Extracted text from ROI
    """
    x, y, w, h = roi_coords
    roi_image = image[y:y+h, x:x+w]
    
    if roi_image.size == 0:
        return ""
    
    processed = preprocess_image(roi_image, preprocess_mode, threshold)
    return extract_text_with_boxes(processed)
