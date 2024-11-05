import easyocr
import os
import base64
from bs4 import BeautifulSoup
import shutil

IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp")
SAVE_HTML_IMGS = False


class OCR:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(["ja", "en"], gpu=True)

    def read_img(self, image_path):
        result = self.reader.readtext(image_path)
        texts = [r[1] for r in result]
        return texts

    def imgs2txt(self, image_paths=None, images_dir=None, save_dir=None):
        assert not (
            image_paths is None and images_dir is None
        ), "image_paths or images_dir must be set."
        # Get save_path
        if image_paths is None:
            save_name = os.path.basename(images_dir)
        else:
            save_name = os.path.basename(image_paths[0])
            save_name = os.path.splitext(save_name)[0]
            images_dir = os.path.dirname(image_paths[0])
        save_dir = images_dir if save_dir is None else save_dir
        save_path = os.path.join(save_dir, "{}.md".format(save_name))
        # Get image_paths
        if image_paths is None:
            image_paths = []
            for root, dirs, files in os.walk(images_dir):
                for file in files:
                    if file.lower().endswith(IMG_EXTS):
                        image_paths.append(os.path.join(root, file))
        # Read images
        ocr_texts = {
            os.path.basename(p): "\n".join(self.read_img(p)) for p in image_paths
        }
        print(ocr_texts)
        # Save text
        sentence = []
        for k, v in ocr_texts.items():
            header = "# {}".format(k)
            merged_text = "{}\n{}\n\n".format(header, v)
            sentence.append(merged_text)
        with open(save_path, "w", encoding="utf-8") as f:
            f.writelines(sentence)

    def html2imgs(self, html_path, image_dir):
        # Read html
        with open(html_path, "r", encoding="utf-8") as f:
            html_data = f.read()

        # Analyze html
        soup = BeautifulSoup(html_data, "html.parser")

        # Convert
        for i, img in enumerate(soup.find_all("img")):
            src = img.get("src")
            if src.startswith("data:image"):
                # Extract image data
                header, data = src.split(",", 1)
                # Decode base64
                image_data = base64.b64decode(data)
                # Get path
                ext = header.split(";")[0].split("/")[1]
                image_path = os.path.join(image_dir, "image{:03}.{}".format(i, ext))
                # Save image
                with open(image_path, "wb") as f:
                    f.write(image_data)
                print(f"Saved image to {image_path}")

    def html2txt(self, html_path):
        # Create image dir
        parent_dir = os.path.dirname(html_path)
        image_name = os.path.basename(html_path)
        image_name = os.path.splitext(image_name)[0]
        image_dir = os.path.join(parent_dir, image_name)
        os.makedirs(image_dir, exist_ok=True)

        # Extract image
        self.html2imgs(html_path, image_dir)

        # OCR image
        self.imgs2txt(images_dir=image_dir, save_dir=parent_dir)

        # Del image
        if not SAVE_HTML_IMGS:
            shutil.rmtree(image_dir, ignore_errors=True)
