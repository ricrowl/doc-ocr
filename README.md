# doc-ocr

This module outputs the text found in images using OCR.
It supports not only image data but also images embedded in HTML.

## Install

Install the required Python packages:
```
pip install -r requirements.txt
```

## Usage

Set source path to .env
- For image dir: `SOURCE_PATH=path/to/images/dir`
- For html path: `SOURCE_PATH=path/to/html/path`

Run the translation script:
```
python src/main.py
```