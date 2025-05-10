import cv2
import numpy as np
from PIL import Image

def ela(image_path, quality=90):
    """Performs Error Level Analysis (ELA) on an image."""
    try:
        original = Image.open(image_path).convert('RGB')
        original.save('temp.jpg', 'JPEG', quality=quality)
        compressed = Image.open('temp.jpg')
        
        # Calculate difference
        diff = np.abs(np.array(original) - np.array(compressed))
        diff = diff.mean(axis=2)  # Convert to grayscale
        diff = (diff * 255).astype(np.uint8)
        
        return diff
    except Exception as e:
        print(f"ELA Error: {e}")
        return None

def preprocess_image(image_path, target_size=(256, 256)):
    """Preprocess image for CNN input."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize
    return img