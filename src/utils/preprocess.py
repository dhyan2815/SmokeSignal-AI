#preprocess.py
#This file is used to preprocess the image before it is fed into the model.

import numpy as np
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available, using PIL fallback")
from PIL import Image

def normalize_image(image_input, target_size=None):
    """
    Normalizes an image by scaling pixel values to the range [0, 1].
    Works with both file paths and PIL images.

    Args:
        image_input (str or PIL.Image): The image file path or PIL Image object.
        target_size (tuple, optional): Target size as (width, height) for resizing.

    Returns:
        numpy.ndarray: The normalized image as a NumPy array, or None if the image cannot be processed.
    """
    try:
        # Handle different input types
        if isinstance(image_input, str):
            # Load from file path
            if CV2_AVAILABLE:
                img = cv2.imread(image_input)
                if img is None:
                    print(f"Error: Could not load image from {image_input}")
                    return None
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                # Fallback to PIL
                img_pil = Image.open(image_input)
                img = np.array(img_pil)
        elif isinstance(image_input, Image.Image):
            # Convert PIL image to numpy array
            img = np.array(image_input)
        else:
            print(f"Error: Unsupported image input type: {type(image_input)}")
            return None

        # Resize if target size is specified
        if target_size is not None:
            if isinstance(image_input, str) and CV2_AVAILABLE:
                # For file paths, use cv2 resize
                img = cv2.resize(img, target_size)
            else:
                # For PIL images or when cv2 not available, use PIL resize
                img_pil = Image.fromarray(img)
                img_pil = img_pil.resize(target_size)
                img = np.array(img_pil)

        # Convert the image to float32 for accurate calculations
        img = img.astype(np.float32)

        # Normalize the image to the range [0, 1]
        normalized_img = img / 255.0

        return normalized_img

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def preprocess_for_model(image_input, model_input_shape):
    """
    Preprocess image specifically for model input.
    
    Args:
        image_input (str or PIL.Image): The image to preprocess
        model_input_shape (tuple): Expected model input shape (height, width, channels)
    
    Returns:
        numpy.ndarray: Preprocessed image ready for model input
    """
    try:
        # Extract target size from model input shape
        if len(model_input_shape) == 3:
            target_size = (model_input_shape[1], model_input_shape[0])  # (width, height)
        else:
            target_size = None
            
        # Normalize image
        normalized_img = normalize_image(image_input, target_size)
        
        if normalized_img is None:
            return None
            
        # Add batch dimension if needed
        if len(model_input_shape) == 3:
            # For image models: (batch, height, width, channels)
            preprocessed = np.expand_dims(normalized_img, axis=0)
        elif len(model_input_shape) == 2:
            # For flattened models: (batch, features)
            preprocessed = normalized_img.reshape(1, -1)
        else:
            raise ValueError(f"Unsupported model input shape: {model_input_shape}")
            
        return preprocessed
        
    except Exception as e:
        print(f"Error preprocessing image for model: {e}")
        return None

def get_image_info(image_input):
    """
    Get basic information about an image.
    
    Args:
        image_input (str or PIL.Image): The image to analyze
    
    Returns:
        dict: Dictionary containing image information
    """
    try:
        if isinstance(image_input, str):
            if CV2_AVAILABLE:
                img = cv2.imread(image_input)
                if img is None:
                    return None
                height, width, channels = img.shape
                format_type = "File (OpenCV)"
            else:
                # Fallback to PIL
                img_pil = Image.open(image_input)
                width, height = img_pil.size
                channels = len(img_pil.getbands())
                format_type = "File (PIL)"
        elif isinstance(image_input, Image.Image):
            width, height = image_input.size
            channels = len(image_input.getbands())
            format_type = "PIL Image"
        else:
            return None
            
        return {
            "format": format_type,
            "width": width,
            "height": height,
            "channels": channels,
            "aspect_ratio": width / height if height > 0 else 0
        }
        
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None