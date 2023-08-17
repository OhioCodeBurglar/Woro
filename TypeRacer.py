import os
import pytesseract
import cv2
from PIL import Image
import numpy as np
import time
import nltk
from nltk.corpus import words as nltk_words
from random import choice

nltk.download("words")

# Path to the "for_bot" folder in Downloads
downloads_path = os.path.expanduser("/home/jose/Pictures")
for_bot_folder = os.path.join(downloads_path, "Screenshots")

# Check if the "for_bot" folder exists
if os.path.exists(for_bot_folder) and os.path.isdir(for_bot_folder):
    while True:
        # List all files in the "for_bot" folder
        image_files = [f for f in os.listdir(for_bot_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if image_files:
            for image_file in image_files:
                # Create the full path to the image
                image_path = os.path.join(for_bot_folder, image_file)

                # Open the image using PIL (Python Imaging Library)
                image = Image.open(image_path)

                # Convert PIL image to NumPy array (OpenCV format)
                image_np = np.array(image)

                # Convert the image to grayscale
                gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

                # Apply Otsu's thresholding to create a binary image
                _, thresholded = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Invert the colors to enhance text visibility and remove underlines
                inverted_image = cv2.bitwise_not(thresholded)

                # Convert OpenCV image back to PIL
                processed_image = Image.fromarray(inverted_image)
                
                # Use Tesseract to extract text from the image
                extracted_text = pytesseract.image_to_string(thresholded)
                words = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,?!;:'()"
                filtered_text = ''.join([ex for ex in extracted_text if ex in words]) 
                extracted_text = filtered_text
                
                # Extract words and replace the first word if not valid
                word_list = extracted_text.strip().split()
                if word_list:
                    first_word = word_list[0]

                    if first_word not in nltk_words.words():
                        valid_words = [word for word in nltk_words.words() if word.isalpha()]
                        new_word = choice(valid_words)
                        word_list[0] = new_word

                    extracted_text = ' '.join(word_list)

                # Print the final extracted text
                print(f"Extracted text from {image_file}:\n{extracted_text}\n")

                # Remove the processed image file
                os.remove(image_path)
        
        # Wait for a few seconds before checking again
        time.sleep(1)
else:
    print("'Screenshots' folder not found in Pictures directory.")

