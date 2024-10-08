import streamlit as st
import cv2
import numpy as np
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import tempfile
from io import BytesIO
import os
import google.generativeai as genai


def generate_barcode(name):
    barcode_writer = ImageWriter()
    barcode = Code128(name, writer=barcode_writer)
    buffer = BytesIO()
    barcode.write(buffer)
    buffer.seek(0)
    return buffer


def create_dummy_barcode():
    img = np.zeros((100, 400, 3), dtype=np.uint8)
    cv2.putText(img, 'BARCODE', (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    return img


def generate_pallet_number():
    return np.random.randint(1000, 9999)

def get_gemini_results():
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction="you are a product information provider. a user will give you any item name, you have to generate its full name, company name and lcoation. if you have then give other wise just display product description and company name.",
        )

        response = model.generate_content()

        print(response.text)

# Streamlit UI
st.title(" AI Product Barcode Creator and Pallet Management")

uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)
    
    create_barcode = st.radio("Do you want to create a barcode?", ("No", "Yes"))
    if create_barcode == "Yes":
        barcode_image_buffer = generate_barcode("Product")
        
        # Display the barcode image from the BytesIO object
        barcode_img = Image.open(barcode_image_buffer)
        st.image(barcode_img, caption='Generated Barcode', use_column_width=True)
        
        # Download button for the barcode image
        st.download_button("Download Barcode", data=barcode_image_buffer, file_name="barcode.png", mime="image/png")
        
        create_pallet = st.radio("Do you want to generate a pallet code?", ("No", "Yes"))
        if create_pallet == "Yes":
            pallet_number = generate_pallet_number()
            st.write(f"Pallet Number: {pallet_number}")
            
            add_distribution_boards = st.radio("Add distribution boards?", ("No", "Yes"))
            if add_distribution_boards == "Yes":
                st.write("Distribution Boards:")
                for i in range(1, 7):
                    st.write(f"Distribution Board {i}")
                
                st.write("Pallet finalized with 6 distribution boards.")
                st.write("Assigning warehouse location to pallet.")
                st.write("Warehouse Location: Warehouse A")

    else:
        st.write("Product Name: Sample Product")
        st.write("Warehouse Location: Warehouse B")
