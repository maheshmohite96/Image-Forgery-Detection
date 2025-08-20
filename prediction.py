import numpy as np
from tensorflow.keras.models import load_model
import os
import tensorflow as tf
from ela import convert_to_ela_image
import warnings
from keras import backend as K
from typing import Tuple

# Constants
DEFAULT_MODEL_NAME = "model.keras"  # Changed from .h5 to .keras
IMAGE_SIZE = (128, 128)
DEFAULT_QUALITY = 90

# Disable TensorFlow warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class ImageForgeryDetector:
    def __init__(self, model_path: str = None):
        """Initialize the detector with optional model path"""
        self.model = None
        # Get the directory where the script is running
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Set default path to model.keras in the same directory
        self.model_path = model_path or os.path.join(script_dir, DEFAULT_MODEL_NAME)
        print(f"Model path being used: {self.model_path}")  # Debug print
        self.load_model()  # Load model immediately on initialization
        
    def prepare_image(self, image_path: str, quality: int = DEFAULT_QUALITY) -> np.ndarray:
        try:
            # Get ELA image
            ela_image = convert_to_ela_image(image_path, quality)
            
            # Convert to PIL Image if needed
            if isinstance(ela_image, np.ndarray):
                ela_image = Image.fromarray(ela_image)
            elif not hasattr(ela_image, 'resize'):
                raise ValueError("ELA function should return PIL Image or numpy array")
            
            # Resize and normalize
            image_array = np.array(ela_image.resize(IMAGE_SIZE)) / 255.0
            
            # Convert grayscale to RGB if needed
            if len(image_array.shape) == 2:
                image_array = np.stack((image_array,)*3, axis=-1)
            elif image_array.shape[2] == 4:  # RGBA case
                image_array = image_array[:, :, :3]
                
            return image_array
            
        except Exception as e:
            raise ValueError(f"Image preparation failed: {str(e)}")

    def load_model(self):
        """Load the trained model"""
        if not os.path.exists(self.model_path):
            available_files = [f for f in os.listdir(os.path.dirname(self.model_path)) 
                            if f.endswith(('.keras', '.h5'))]
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}\n"
                f"Available model files: {available_files}"
            )
        self.model = load_model(self.model_path)
        print("✅ Model loaded successfully")  # Confirmation

    def predict(self, image_path: str) -> Tuple[str, float]:
        """
        Predict whether an image is forged or authentic
        Args:
            image_path: Path to the input image
        Returns:
            tuple: (prediction, confidence)
        Raises:
            ValueError: If prediction fails
        """
        try:
            # Validate inputs
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            if self.model is None:
                self.load_model()

            # Prepare image
            test_image = self.prepare_image(image_path)
            test_image = test_image.reshape(-1, *IMAGE_SIZE, 3)

            # Make prediction
            y_pred = self.model.predict(test_image)
            y_pred_class = int(round(y_pred[0][0]))
            
            # Get class names and confidence
            class_names = ["Forged", "Authentic"]
            prediction = class_names[y_pred_class]
            confidence = (1 - y_pred[0][0]) * 100 if y_pred_class == 0 else y_pred[0][0] * 100
            
            return prediction, round(confidence, 2)
            
        except Exception as e:
            K.clear_session()
            raise ValueError(f"Prediction failed: {str(e)}")
        finally:
            K.clear_session()

if __name__ == "__main__":
    try:
        print("Current working directory:", os.getcwd())
        print("Files in directory:", os.listdir())
        
        # Initialize detector
        detector = ImageForgeryDetector()
        
        # Test the prediction
        test_image_path = r"C:\Users\hp\Desktop\image-forgery-detection-main\dataset\CASIA1\Au\Au_ani_0001.jpg"
        
        if os.path.exists(test_image_path):
            pred, conf = detector.predict(test_image_path)
            print(f"Prediction: {pred}\nConfidence: {conf}%")
        else:
            print(f"Test image not found: {test_image_path}")
            
    except Exception as e:
        print(f"Error: {str(e)}")