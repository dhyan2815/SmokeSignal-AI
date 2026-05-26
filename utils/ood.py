import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np
from PIL import Image

class OODDetector:
    """
    Out-of-Distribution Detector using MobileNetV2.
    Determines if an image is likely a satellite/aerial view or something else (OOD).
    """
    
    def __init__(self):
        # Load pre-trained MobileNetV2 for scene classification
        # We use ImageNet weights to identify common non-satellite objects
        self.model = MobileNetV2(weights='imagenet')
        
        # Categories that strongly indicate OOD for this specific app (non-satellite)
        self.OOD_KEYWORDS = [
            'web_site', 'menu', 'envelope', 'monitor', 'screen', 'television',
            'banner', 'poster', 'label', 'comic_book', 'book_jacket',
            'crossword_puzzle', 'scoreboard', 'digital_clock', 'wall_clock',
            'cellular_telephone', 'hand-held_computer', 'notebook', 'desktop_computer'
        ]
        
        # Categories that indicate valid geospatial/aerial scenes
        self.VALID_KEYWORDS = [
            'valley', 'mountain', 'cliff', 'promontory', 'lakeside', 'seashore',
            'geyser', 'volcano', 'island', 'coral_reef', 'airliner', 'warplane',
            'space_shuttle', 'earthstar', 'mushroom' # Sometimes satellite views look like textures
        ]

    def check_image(self, img):
        """
        Check if an image is Out-of-Distribution.
        
        Args:
            img (PIL.Image): Input image
            
        Returns:
            bool: True if OOD, False if likely valid
            str: Description of the detected scene
            float: Confidence in the scene classification
        """
        try:
            # Prepare image for MobileNetV2 (224x224)
            img_resized = img.resize((224, 224))
            x = np.array(img_resized)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            
            # Predict
            preds = self.model.predict(x, verbose=0)
            decoded = decode_predictions(preds, top=5)[0]
            
            # Extract top prediction
            top_label = decoded[0][1]
            top_conf = float(decoded[0][2])
            
            # Logic: Check if any of the top 3 labels are in OOD keywords
            is_ood = False
            scene_description = top_label
            
            for i in range(3):
                label = decoded[i][1].lower()
                if any(keyword in label for keyword in self.OOD_KEYWORDS):
                    is_ood = True
                    scene_description = label
                    break
            
            # Double check: If the top prediction is NOT a geospatial keyword but has high confidence
            # we might still flag it if it doesn't look like an aerial texture.
            # For now, the keyword approach is robust for "LinkedIn banners" and "UI screenshots".
            
            return is_ood, scene_description.replace('_', ' '), top_conf
            
        except Exception as e:
            print(f"Error in OOD Detection: {e}")
            return False, "Unknown", 0.0

# Singleton instance to avoid reloading model
_detector = None

def is_ood(img):
    global _detector
    if _detector is None:
        _detector = OODDetector()
    return _detector.check_image(img)
