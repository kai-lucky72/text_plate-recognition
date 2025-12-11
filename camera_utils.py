#!/usr/bin/env python3
"""
Camera Utilities - Handles webcam/camera capture using OpenCV.
Provides continuous frame capture for live camera feed.
"""

import cv2
import numpy as np


class CameraCapture:
    """Wrapper class for OpenCV camera capture."""
    
    def __init__(self, camera_index=0):
        """
        Initialize camera capture.
        
        Args:
            camera_index: Camera device index (default: 0 for primary camera)
        """
        self.camera = None
        self.camera_index = camera_index
        self.is_open = False
        self.frame_count = 0
        
        try:
            self.camera = cv2.VideoCapture(camera_index)
            
            # Set camera properties for better performance
            if self.camera.isOpened():
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
                self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
                
                self.is_open = True
            else:
                print(f"Warning: Could not open camera {camera_index}")
                self.is_open = False
        
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.is_open = False
    
    def get_frame(self):
        """
        Capture and return a single frame from the camera.
        
        Returns:
            Frame as numpy array (BGR format) or None if capture fails
        """
        if not self.is_open or self.camera is None:
            return None
        
        try:
            success, frame = self.camera.read()
            
            if success:
                self.frame_count += 1
                return frame
            else:
                return None
        
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def get_frame_with_delay(self, delay_ms=33):
        """
        Capture frame with specified delay between reads.
        
        Args:
            delay_ms: Delay in milliseconds (default 33ms ≈ 30fps)
        
        Returns:
            Frame as numpy array (BGR format) or None
        """
        frame = self.get_frame()
        cv2.waitKey(delay_ms)
        return frame
    
    def release(self):
        """Release the camera resource."""
        if self.camera is not None:
            self.camera.release()
            self.is_open = False
    
    def is_available(self):
        """Check if camera is available and open."""
        return self.is_open
    
    def get_frame_count(self):
        """Get total number of frames captured."""
        return self.frame_count
    
    def reset_frame_count(self):
        """Reset frame counter."""
        self.frame_count = 0
    
    def set_resolution(self, width, height):
        """
        Set camera resolution.
        
        Args:
            width: Frame width in pixels
            height: Frame height in pixels
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            return False
        
        try:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            return True
        except Exception as e:
            print(f"Error setting resolution: {e}")
            return False
    
    def set_fps(self, fps):
        """
        Set camera FPS.
        
        Args:
            fps: Frames per second
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_open:
            return False
        
        try:
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            return True
        except Exception as e:
            print(f"Error setting FPS: {e}")
            return False
    
    def get_resolution(self):
        """
        Get current camera resolution.
        
        Returns:
            Tuple of (width, height)
        """
        if not self.is_open:
            return (0, 0)
        
        try:
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        except:
            return (0, 0)


def test_camera_availability():
    """
    Test if camera is available and accessible.
    
    Returns:
        True if camera is available, False otherwise
    """
    try:
        camera = cv2.VideoCapture(0)
        available = camera.isOpened()
        camera.release()
        return available
    except:
        return False
