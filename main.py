from src.ocr_handler import *

print("Welcome to OCR video processer.")
filename = input("ENTER FILENAME: ")

ocr_type = input("ENTER OCR_MODE (WORDS/LINES): ")

# Add a prompt for the target language
target_language = input("ENTER TARGET LANGUAGE (e.g., 'en' for English, 'es' for Spanish): ")


if os.path.isfile(filename):
    ocr_handler = OCR_HANDLER(filename, CV2_HELPER(),ocr_type, target_language)
    ocr_handler.process_frames()
    ocr_handler.assemble_video()
    print("OCR PROCESS FINISHED: OUTPUT FILE => " + ocr_handler.out_name)

else:
    print("FILE NOT FOUND: BYE")
