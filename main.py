import streamlit as st
import os
from PIL import Image
import numpy as np
from steganography import encode_message, decode_message
from utils import validate_image_for_message, save_image, resize_image

st.set_page_config(
    page_title="Image Steganography",
    layout="wide"
)

def main():
    st.title("Image Steganography")
    st.markdown("""
    """)

    tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

    with tab1:
        st.header("Hide a Message")

        cover_image = st.file_uploader("Upload Cover Image (PNG, JPG)", type=['png', 'jpg', 'jpeg'], key="cover")
        if cover_image:
            try:
                original_img = Image.open(cover_image)
                # Show original dimensions
                st.info(f"Original image dimensions: {original_img.size[0]}x{original_img.size[1]}")

                # Resize image if needed
                cover_img = resize_image(original_img)
                st.image(cover_img, caption="Cover Image (Resized)", use_container_width=True)

                # Show new dimensions if image was resized
                if cover_img.size != original_img.size:
                    st.info(f"Resized to: {cover_img.size[0]}x{cover_img.size[1]}")
            except Exception as e:
                st.error(f"Error loading cover image: {str(e)}")
                cover_img = None

        message = st.text_area("Enter your secret message", height=100)

        if st.button("Hide Message", key="hide") and cover_image and message:
            with st.spinner("Processing..."):
                try:
                    if validate_image_for_message(cover_img, message):
                        encoded_image = encode_message(cover_img, message)
                        st.success("Message hidden successfully!")

                        # Display the result
                        st.image(encoded_image, caption="Result Image", use_container_width=True)

                        # Save option
                        if st.download_button(
                            label="Download Encoded Image",
                            data=save_image(encoded_image),
                            file_name="encoded_image.png",
                            mime="image/png"
                        ):
                            st.success("Image downloaded successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    with tab2:
        st.header("Extract Hidden Message")

        encoded_upload = st.file_uploader("Upload Encoded Image (PNG)", type=['png'], key="encoded")

        if encoded_upload:
            try:
                encoded_img = Image.open(encoded_upload)
                st.image(encoded_img, caption="Encoded Image", use_container_width=True)
                st.info(f"Image dimensions: {encoded_img.size[0]}x{encoded_img.size[1]}")

                if st.button("Extract Hidden Message", key="extract"):
                    with st.spinner("Extracting hidden message..."):
                        try:
                            decoded_message = decode_message(encoded_img)
                            st.success("Message extracted successfully!")

                            # Display the extracted message in a text area
                            st.text_area("Extracted Message", decoded_message, height=100, key="decoded")
                        except Exception as e:
                            st.error(f"Failed to extract message: {str(e)}")
            except Exception as e:
                st.error(f"Error loading encoded image: {str(e)}")

if __name__ == "__main__":
    main()