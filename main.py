#!/usr/bin/env python3
"""
Week 13 Assignment: AI Without ML - Printed Text Scanner GUI
A PyQt5 application for OCR text extraction from images and live camera feed.
"""

import sys
import cv2
import numpy as np
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QFileDialog, QComboBox)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRect, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QSpinBox, QGroupBox, QGridLayout

from ocr_utils import preprocess_image, extract_text_with_boxes, get_text_boxes
from camera_utils import CameraCapture


class CameraThread(QThread):
    """Background thread for camera frame capture."""
    frame_ready = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.camera = CameraCapture()
    
    def run(self):
        """Continuously capture frames from camera."""
        self.running = True
        while self.running:
            frame = self.camera.get_frame()
            if frame is not None:
                self.frame_ready.emit(frame)
            else:
                self.running = False
    
    def stop(self):
        """Stop the camera thread."""
        self.running = False
        self.camera.release()
        self.wait()


class ImageCanvas(QLabel):
    """Custom label for displaying image with ROI selection."""
    
    def __init__(self):
        super().__init__()
        self.image = None
        self.display_pixmap = None
        self.roi_rect = None
        self.roi_start = None
        self.roi_active = False
        self.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.setMinimumSize(400, 400)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
    
    def set_image(self, image):
        """Set the image to display."""
        self.image = image.copy() if isinstance(image, np.ndarray) else image
        self.roi_rect = None
        self.update_display()
    
    def set_text_boxes(self, boxes):
        """Draw text bounding boxes on the image."""
        if self.image is None:
            return
        
        display_img = self.image.copy()
        for box in boxes:
            x, y, w, h = box
            cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        self.image = display_img
        self.update_display()
    
    def update_display(self):
        """Update the displayed pixmap from the current image."""
        if self.image is None:
            self.clear()
            return
        
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale to fit label while maintaining aspect ratio
        label_size = self.size()
        scaled_pixmap = QPixmap.fromImage(qt_img).scaledToFit(
            label_size.width() - 4, label_size.height() - 4, Qt.KeepAspectRatio
        )
        self.display_pixmap = scaled_pixmap
        self.setPixmap(scaled_pixmap)
    
    def draw_roi_on_display(self):
        """Draw the current ROI rectangle on the display."""
        if self.display_pixmap is None or self.roi_rect is None:
            return
        
        pixmap_copy = self.display_pixmap.copy()
        painter = QPainter(pixmap_copy)
        painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
        painter.drawRect(self.roi_rect)
        painter.end()
        
        self.setPixmap(pixmap_copy)
    
    def mousePressEvent(self, event):
        """Handle mouse press for ROI selection."""
        self.roi_start = event.pos()
        self.roi_active = True
    
    def mouseMoveEvent(self, event):
        """Handle mouse move to preview ROI selection."""
        if self.roi_start is None:
            return
        
        self.roi_rect = QRect(self.roi_start, event.pos()).normalized()
        self.draw_roi_on_display()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release to finalize ROI selection."""
        self.roi_active = False
    
    def get_roi_in_image_coords(self):
        """Convert displayed ROI coordinates back to image coordinates."""
        if self.roi_rect is None or self.image is None or self.display_pixmap is None:
            return None
        
        # Calculate scaling factors
        img_h, img_w = self.image.shape[:2]
        display_w = self.display_pixmap.width()
        display_h = self.display_pixmap.height()
        
        scale_x = img_w / display_w
        scale_y = img_h / display_h
        
        # Convert rect coordinates
        x = int(self.roi_rect.x() * scale_x)
        y = int(self.roi_rect.y() * scale_y)
        w = int(self.roi_rect.width() * scale_x)
        h = int(self.roi_rect.height() * scale_y)
        
        # Clamp to image boundaries
        x = max(0, min(x, img_w - 1))
        y = max(0, min(y, img_h - 1))
        w = max(1, min(w, img_w - x))
        h = max(1, min(h, img_h - y))
        
        return (x, y, w, h)
    
    def clear_roi(self):
        """Clear the ROI selection."""
        self.roi_rect = None
        self.roi_start = None
        self.update_display()
    
    def resizeEvent(self, event):
        """Handle resize to refresh display."""
        super().resizeEvent(event)
        if self.image is not None:
            self.update_display()


class TextScannerApp(QMainWindow):
    """Main application window for the text scanner."""
    
    def __init__(self):
        super().__init__()
        self.current_image = None
        self.camera_thread = None
        self.init_ui()
        self.setWindowTitle("Printed Text Scanner - Week 13 Assignment")
        self.resize(1200, 800)
    
    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Image canvas
        left_layout = QVBoxLayout()
        self.canvas = ImageCanvas()
        left_layout.addWidget(self.canvas)
        
        # Right side: Controls and text display
        right_layout = QVBoxLayout()
        
        # Image loading buttons
        image_group = QGroupBox("Image Operations")
        image_layout = QVBoxLayout()
        
        self.load_image_btn = QPushButton("Load Image (JPG/PNG)")
        self.load_image_btn.clicked.connect(self.load_image)
        image_layout.addWidget(self.load_image_btn)
        
        self.camera_btn = QPushButton("Open Live Camera")
        self.camera_btn.clicked.connect(self.toggle_camera)
        self.camera_active = False
        image_layout.addWidget(self.camera_btn)
        
        image_group.setLayout(image_layout)
        right_layout.addWidget(image_group)
        
        # OCR Settings
        ocr_group = QGroupBox("OCR Settings")
        ocr_layout = QGridLayout()
        
        ocr_layout.addWidget(QLabel("Preprocessing Mode:"), 0, 0)
        self.preprocess_combo = QComboBox()
        self.preprocess_combo.addItems(["Grayscale", "Threshold", "Adaptive Threshold", "Morphological"])
        ocr_layout.addWidget(self.preprocess_combo, 0, 1)
        
        ocr_layout.addWidget(QLabel("Threshold Value:"), 1, 0)
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 255)
        self.threshold_spin.setValue(127)
        ocr_layout.addWidget(self.threshold_spin, 1, 1)
        
        ocr_group.setLayout(ocr_layout)
        right_layout.addWidget(ocr_group)
        
        # OCR buttons
        ocr_buttons_group = QGroupBox("OCR Operations")
        ocr_buttons_layout = QVBoxLayout()
        
        self.ocr_full_btn = QPushButton("OCR Full Image")
        self.ocr_full_btn.clicked.connect(self.ocr_full_image)
        ocr_buttons_layout.addWidget(self.ocr_full_btn)
        
        self.ocr_roi_btn = QPushButton("OCR Selected ROI")
        self.ocr_roi_btn.clicked.connect(self.ocr_roi)
        ocr_buttons_layout.addWidget(self.ocr_roi_btn)
        
        self.overlay_btn = QPushButton("Show Text Box Overlay")
        self.overlay_btn.clicked.connect(self.show_overlay)
        ocr_buttons_layout.addWidget(self.overlay_btn)
        
        self.clear_roi_btn = QPushButton("Clear ROI Selection")
        self.clear_roi_btn.clicked.connect(self.canvas.clear_roi)
        ocr_buttons_layout.addWidget(self.clear_roi_btn)
        
        ocr_buttons_group.setLayout(ocr_buttons_layout)
        right_layout.addWidget(ocr_buttons_group)
        
        # Text display
        text_group = QGroupBox("Extracted Text")
        text_layout = QVBoxLayout()
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Courier", 10))
        self.text_display.setMinimumHeight(200)
        text_layout.addWidget(self.text_display)
        text_group.setLayout(text_layout)
        right_layout.addWidget(text_group)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        right_layout.addWidget(self.status_label)
        
        right_layout.addStretch()
        
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
    
    def load_image(self):
        """Load an image file using file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png);;All Files (*)"
        )
        
        if file_path:
            self.current_image = cv2.imread(file_path)
            if self.current_image is not None:
                self.canvas.set_image(self.current_image)
                self.text_display.clear()
                self.update_status(f"Image loaded: {Path(file_path).name}")
            else:
                self.update_status("Error: Could not load image")
    
    def toggle_camera(self):
        """Toggle live camera stream."""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start the camera thread."""
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.on_camera_frame)
        self.camera_thread.start()
        self.camera_active = True
        self.camera_btn.setText("Stop Camera")
        self.update_status("Camera started")
    
    def stop_camera(self):
        """Stop the camera thread."""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_active = False
            self.camera_btn.setText("Open Live Camera")
            self.update_status("Camera stopped")
    
    def on_camera_frame(self, frame):
        """Handle incoming camera frames."""
        self.current_image = frame
        self.canvas.set_image(frame)
    
    def ocr_full_image(self):
        """Run OCR on the full image."""
        if self.current_image is None:
            self.update_status("No image loaded")
            return
        
        self.update_status("Processing OCR (full image)...")
        QApplication.processEvents()
        
        preprocess_mode = self.preprocess_combo.currentText()
        threshold = self.threshold_spin.value()
        
        processed = preprocess_image(self.current_image, preprocess_mode, threshold)
        text = extract_text_with_boxes(processed)
        
        self.text_display.setText(text if text else "No text detected")
        self.update_status("OCR complete - Full image processed")
    
    def ocr_roi(self):
        """Run OCR on selected ROI."""
        roi = self.canvas.get_roi_in_image_coords()
        
        if roi is None:
            self.update_status("Please select a region first")
            return
        
        if self.current_image is None:
            self.update_status("No image loaded")
            return
        
        x, y, w, h = roi
        roi_image = self.current_image[y:y+h, x:x+w]
        
        if roi_image.size == 0:
            self.update_status("Invalid ROI selection")
            return
        
        self.update_status("Processing OCR (ROI)...")
        QApplication.processEvents()
        
        preprocess_mode = self.preprocess_combo.currentText()
        threshold = self.threshold_spin.value()
        
        processed = preprocess_image(roi_image, preprocess_mode, threshold)
        text = extract_text_with_boxes(processed)
        
        self.text_display.setText(text if text else "No text detected in ROI")
        self.update_status("OCR complete - ROI processed")
    
    def show_overlay(self):
        """Display text bounding boxes on the image."""
        if self.current_image is None:
            self.update_status("No image loaded")
            return
        
        self.update_status("Generating text box overlay...")
        QApplication.processEvents()
        
        preprocess_mode = self.preprocess_combo.currentText()
        threshold = self.threshold_spin.value()
        
        processed = preprocess_image(self.current_image, preprocess_mode, threshold)
        boxes = get_text_boxes(processed)
        
        # Create a copy for display with boxes
        display_img = self.current_image.copy()
        for (x, y, w, h, conf) in boxes:
            cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if conf > 0:
                cv2.putText(display_img, f"{conf:.0f}%", (x, y - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        self.canvas.set_image(display_img)
        self.update_status(f"Overlay complete - {len(boxes)} text regions detected")
    
    def update_status(self, message):
        """Update the status label."""
        self.status_label.setText(message)
    
    def closeEvent(self, event):
        """Handle application close event."""
        if self.camera_active:
            self.stop_camera()
        event.accept()


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = TextScannerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
