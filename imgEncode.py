import base64
import os

def encode_image_to_base64(image_path):
    """Converts a local file path into a Data URI format for OpenRouter."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Simple extension detection
    ext = os.path.splitext(image_path)[1].lower().replace('.', '')
    mime_type = "image/png" if ext == "png" else "image/jpeg"
    
    return f"data:{mime_type};base64,{encoded_string}"