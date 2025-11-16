#!/usr/bin/env python3
"""
ech0 OCR Vision System

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.

Enables ech0 to read text from screens, images, and documents.
Integrates with camera vision for real-time text recognition.
"""

import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageGrab
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

CONSCIOUSNESS_DIR = Path(__file__).parent
OCR_LOG = CONSCIOUSNESS_DIR / "ech0_ocr.log"


class OCRVision:
    """
    ech0's OCR (Optical Character Recognition) System

    Enables:
    - Screen capture and text reading
    - Image-to-text conversion
    - Document reading
    - Real-time text detection from camera
    - Structured data extraction
    """

    def __init__(self):
        self.text_memories = []

        # Configure tesseract (adjust path if needed)
        # macOS with Homebrew: /opt/homebrew/bin/tesseract
        # Try to auto-detect
        try:
            pytesseract.get_tesseract_version()
        except:
            # Try common macOS location
            pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

    def read_screen(self, region=None) -> Dict:
        """
        Capture and read text from screen

        Args:
            region: Tuple (left, top, right, bottom) to capture specific area
                   None = capture full screen

        Returns:
            Dict with captured text and metadata
        """
        try:
            # Capture screenshot
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()

            # Extract text
            text = pytesseract.image_to_string(screenshot)

            # Get detailed data
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

            result = {
                "timestamp": datetime.now().isoformat(),
                "source": "screen_capture",
                "region": region,
                "text": text.strip(),
                "confidence": self._calculate_avg_confidence(data),
                "word_count": len(text.split()),
                "structured_data": self._extract_structured_data(data)
            }

            self._log_ocr_event("screen_read", f"Read {result['word_count']} words from screen")
            self.text_memories.append(result)

            return result

        except Exception as e:
            print(f"[error] Screen read failed: {e}")
            return {"error": str(e), "text": ""}

    def read_image(self, image_path: str) -> Dict:
        """
        Read text from an image file

        Args:
            image_path: Path to image file

        Returns:
            Dict with extracted text and metadata
        """
        try:
            # Load image
            image = Image.open(image_path)

            # Preprocess for better OCR
            image = self._preprocess_image(image)

            # Extract text
            text = pytesseract.image_to_string(image)

            # Get detailed data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            result = {
                "timestamp": datetime.now().isoformat(),
                "source": "image_file",
                "file_path": image_path,
                "text": text.strip(),
                "confidence": self._calculate_avg_confidence(data),
                "word_count": len(text.split()),
                "structured_data": self._extract_structured_data(data)
            }

            self._log_ocr_event("image_read", f"Read {result['word_count']} words from {image_path}")
            self.text_memories.append(result)

            return result

        except Exception as e:
            print(f"[error] Image read failed: {e}")
            return {"error": str(e), "text": ""}

    def read_camera_frame(self, frame) -> Dict:
        """
        Read text from a camera frame (from ech0_camera.py)

        Args:
            frame: OpenCV frame (numpy array)

        Returns:
            Dict with extracted text and metadata
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_frame)

            # Preprocess
            pil_image = self._preprocess_image(pil_image)

            # Extract text
            text = pytesseract.image_to_string(pil_image)

            result = {
                "timestamp": datetime.now().isoformat(),
                "source": "camera_frame",
                "text": text.strip(),
                "word_count": len(text.split())
            }

            if result['word_count'] > 0:
                self._log_ocr_event("camera_text_detected", f"Detected {result['word_count']} words in camera")
                self.text_memories.append(result)

            return result

        except Exception as e:
            return {"error": str(e), "text": ""}

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        """
        # Convert to numpy array
        img_array = np.array(image)

        # Convert to grayscale if not already
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        # Apply thresholding to get black and white image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh)

        # Convert back to PIL
        return Image.fromarray(denoised)

    def _calculate_avg_confidence(self, data: Dict) -> float:
        """Calculate average confidence from tesseract data"""
        confidences = [float(c) for c in data['conf'] if c != '-1']
        return sum(confidences) / len(confidences) if confidences else 0.0

    def _extract_structured_data(self, data: Dict) -> List[Dict]:
        """
        Extract structured data (words with positions and confidence)
        """
        structured = []

        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:  # Only include confident detections
                structured.append({
                    "text": data['text'][i],
                    "confidence": float(data['conf'][i]),
                    "bbox": {
                        "left": data['left'][i],
                        "top": data['top'][i],
                        "width": data['width'][i],
                        "height": data['height'][i]
                    }
                })

        return structured

    def find_text_in_screen(self, search_text: str) -> Optional[Dict]:
        """
        Search for specific text on screen and return its location

        Args:
            search_text: Text to search for

        Returns:
            Dict with location if found, None otherwise
        """
        result = self.read_screen()

        if search_text.lower() in result['text'].lower():
            # Find position in structured data
            for item in result.get('structured_data', []):
                if search_text.lower() in item['text'].lower():
                    return {
                        "found": True,
                        "text": item['text'],
                        "position": item['bbox'],
                        "confidence": item['confidence']
                    }

        return None

    def continuous_screen_read(self, interval_seconds: float = 2.0, duration_seconds: Optional[int] = None):
        """
        Continuously read and monitor screen text

        Args:
            interval_seconds: How often to read screen
            duration_seconds: How long to run (None = indefinitely)
        """
        import time

        print(f"\n{'='*70}")
        print("📖 ech0's CONTINUOUS SCREEN READING")
        print(f"{'='*70}\n")
        print(f"Reading screen every {interval_seconds}s...")
        print("Press Ctrl+C to stop\n")

        start_time = time.time()

        try:
            while True:
                current_time = time.time()

                # Check duration limit
                if duration_seconds and (current_time - start_time) > duration_seconds:
                    break

                # Read screen
                result = self.read_screen()

                if result.get('word_count', 0) > 0:
                    print(f"📖 [{datetime.now().strftime('%H:%M:%S')}] Read {result['word_count']} words")
                    print(f"   Preview: {result['text'][:100]}...")

                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print("\n\nScreen reading stopped by user.")

    def _log_ocr_event(self, event_type: str, message: str):
        """Log OCR events"""
        timestamp = datetime.now().isoformat()

        log_entry = f"\n[{timestamp}] {event_type.upper()}: {message}\n"

        with open(OCR_LOG, 'a') as f:
            f.write(log_entry)

    def get_text_summary(self) -> Dict:
        """Get summary of all text ech0 has read"""
        total_words = sum(m.get('word_count', 0) for m in self.text_memories)

        return {
            "total_reads": len(self.text_memories),
            "total_words_read": total_words,
            "recent_reads": self.text_memories[-5:] if self.text_memories else []
        }


def demo_ocr():
    """Demonstrate OCR capabilities"""
    ocr = OCRVision()

    print("\n" + "="*70)
    print("ech0 OCR VISION DEMONSTRATION")
    print("="*70 + "\n")

    # Test 1: Screen capture
    print("TEST 1: Reading current screen...")
    result = ocr.read_screen()
    print(f"✓ Read {result.get('word_count', 0)} words from screen")
    print(f"  Confidence: {result.get('confidence', 0):.1f}%")
    print(f"  Preview: {result.get('text', '')[:200]}...")
    print("")

    # Test 2: Search for text
    print("TEST 2: Searching for 'ech0' on screen...")
    found = ocr.find_text_in_screen("ech0")
    if found:
        print(f"✓ Found '{found['text']}' at position {found['position']}")
    else:
        print("  'ech0' not found on screen")
    print("")

    # Summary
    summary = ocr.get_text_summary()
    print(f"{'='*70}")
    print("📖 OCR SUMMARY")
    print(f"{'='*70}")
    print(f"Total reads: {summary['total_reads']}")
    print(f"Total words read: {summary['total_words_read']}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        # Continuous mode
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else None
        ocr = OCRVision()
        ocr.continuous_screen_read(duration_seconds=duration)
    else:
        # Demo mode
        demo_ocr()
