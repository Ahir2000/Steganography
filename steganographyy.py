import numpy as np
from PIL import Image

def text_to_binary(text):
    """Convert text to binary string"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary):
    """Convert binary string to text"""
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:  # Ensure we have a complete byte
            text += chr(int(byte, 2))
    return text

def encode_message(cover_image, message):
    """
    Encode a text message within a cover image using LSB steganography
    """
    cover = np.array(cover_image)

 
    binary_message = text_to_binary(message)
    binary_message += '1111111111111110'  # Add delimiter to mark end of message

    max_bytes = (cover.shape[0] * cover.shape[1] * 3) // 8
    if len(binary_message) > max_bytes * 8:
        raise ValueError(f"Message too long. Maximum {max_bytes} bytes allowed.")

    
    encoded = cover.copy()
    flat_cover = encoded.reshape(-1)
    binary_length = len(binary_message)

    for i in range(binary_length):
        flat_cover[i] = (flat_cover[i] & 0xFE) | int(binary_message[i])

    encoded = flat_cover.reshape(cover.shape)

    return Image.fromarray(encoded)

def decode_message(encoded_image):
    """
    Extract the hidden message from an encoded image
    """

    encoded = np.array(encoded_image)


    flat_encoded = encoded.reshape(-1)

    binary_message = ''
    delimiter = '1111111111111110'

    for i in range(len(flat_encoded)):
        binary_message += str(flat_encoded[i] & 1)
        if len(binary_message) >= 16 and binary_message[-16:] == delimiter:
            binary_message = binary_message[:-16]
            break

    return binary_to_text(binary_message)