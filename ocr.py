import sys
import cv2
import pytesseract
from PIL import Image
import os 

output_dir = 'processed_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def save_image(image, filename):
    """Helper function to save an image to the specified path."""
    cv2.imwrite(os.path.join(output_dir, filename), image)

def process_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)

    # Perform OCR
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_script.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        text = process_image(image_path)
        print(text)
    except Exception as e:
        print(f"Error processing the image: {e}")
        sys.exit(1)
