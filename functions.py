import io
from PIL import Image

def resize_image(image, max_dimension=800):
    """
    Resize image while maintaining aspect ratio
    """
    width, height = image.size
    if width <= max_dimension and height <= max_dimension:
        return image

   
    if width > height:
        new_width = max_dimension
        new_height = int(height * (max_dimension / width))
    else:
        new_height = max_dimension
        new_width = int(width * (max_dimension / height))

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def validate_image_for_message(cover_img, message):
    """
    Validate that the image is suitable for hiding the message
    """
    if cover_img.mode != "RGB":
        raise ValueError("Cover image must be in RGB format")

    # Calculate maximum message size (3 bits per pixel)
    max_bytes = (cover_img.size[0] * cover_img.size[1] * 3) // 8
    message_bytes = len(message.encode('utf-8'))

    if message_bytes > max_bytes:
        raise ValueError(f"Message too long. Maximum {max_bytes} bytes allowed.")

    return True

def save_image(image):
    """
    Convert PIL Image to bytes for downloading
    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr