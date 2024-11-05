from libs import OCR
import os
from dotenv import load_dotenv

load_dotenv()

# Directories of image dir or html files
SOURCE_PATH = os.environ.get("SOURCE_PATH")


def main():
    ocr = OCR()
    ext = os.path.splitext(SOURCE_PATH)[1]
    if ext == "":
        ocr.imgs2txt(images_dir=SOURCE_PATH)
    elif ext == ".html":
        ocr.html2txt(html_path=SOURCE_PATH)
    else:
        print("Unsupported file type")


if __name__ == "__main__":
    main()
