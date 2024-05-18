import os
import pytesseract
import cv2
from pathlib import Path
from googletrans import Translator, LANGUAGES
from langdetect import detect
import numpy as np
from PIL import ImageFont, ImageDraw, Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.threshold(gray,0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return gray

# Define the function for OCR and translation
def object_char_recognition(filename, target='ru'):
    # Initialize the Tesseract and Google Translate
    translator = Translator()
    
    # Read the image using OpenCV
    image = cv2.imread(str(filename))
    if image is None:
        raise FileNotFoundError(f"Image file not found: {filename}")
    
    # Preprocess the image for better OCR results
    preprocessed_image = preprocess_image(image)
    
    # Perform OCR on the image
    custom_config = r'--oem 3 --psm 6'
    ocr_result = pytesseract.image_to_data(preprocessed_image, config=custom_config, output_type=pytesseract.Output.DICT)
    
    # Get the detected text and their positions
    n_boxes = len(ocr_result['level'])
    detected_texts = []
    for i in range(n_boxes):
        if int(float(ocr_result['conf'][i])) > 60 and ocr_result['text'][i].strip():
            (x, y, w, h) = (ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i])
            detected_texts.append({
                'text': ocr_result['text'][i],
                'pos': (x, y, w, h)
            })
    
    # Print detected text for debugging
    print("Detected texts:", detected_texts)

    # Detect the language of the text
    all_text = ' '.join([item['text'] for item in detected_texts])
    detected_language = detect(all_text)
    print(f"Detected language: {LANGUAGES[detected_language]}")
    
    # Translate the text to the target language
    translated_texts = []
    for item in detected_texts:
        try:
            translated_text = translator.translate(item['text'], src=detected_language, dest=target).text
            translated_texts.append({
                'text': translated_text,
                'pos': item['pos']
            })
        except Exception as e: 
            print(f"Error translating text '{item['text']}': {e}")
            translated_texts.append({
                'text': item['text'],
                'pos': item['pos']
            })

    # Print translated texts for debugging
    print("Translated texts:", translated_texts)

    # Convert the image to RGB (PIL format)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Use a font that supports Russian characters
    font_path = "D:\\Realtime-Text-Recognition-in-Video\\DejaVuSans-Bold.ttf"  # Example: "path_to_your_font.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    font = ImageFont.truetype(font_path, 16)
    draw = ImageDraw.Draw(pil_image)

    # Overlay the translated text on the image
    # Overlay the translated text on the image
    for item in translated_texts:
        x, y, w, h = item['pos']
        draw.rectangle([(x, y), (x + w, y + h)], fill=(255, 255, 255))
        draw.text((x, y), item['text'], font=font, fill=(0, 0, 0))

    # Convert back to OpenCV format
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Save the output image
    output_filename = filename.stem + '_translated' + filename.suffix
    output_path = filename.parent / output_filename
    cv2.imwrite(str(output_path), image)
    print(f"Translated image saved as: {output_path}")

if __name__ == '__main__':
    current_filepath = Path(__file__).resolve().parent
    image_filename = current_filepath / 'ocr-sample2.png'
    object_char_recognition(image_filename, target='ru')
