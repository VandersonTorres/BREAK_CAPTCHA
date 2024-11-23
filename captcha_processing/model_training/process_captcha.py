import os

import cv2
import glob
from PIL import Image

os.makedirs("captcha_processing/preprocessing/processed", exist_ok=True)


def process_images(origin_folder, destination_folder="captcha_processing/preprocessing/processed"):
    files = glob.glob(f"{origin_folder}/*")
    for file in files:
        image = cv2.imread(file)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, processed_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        file_name = os.path.basename(file)
        cv2.imwrite(f"{destination_folder}/{file_name}", processed_image)

    files = glob.glob(f"{destination_folder}/*")
    for file in files:
        image = Image.open(file)
        image = image.convert("P")
        image2 = Image.new("P", image.size, (255, 255, 255))
        for x in range(image.size[1]):
            for y in range(image.size[0]):
                pixel_color = image.getpixel((y, x))
                if pixel_color < 115:
                    image2.putpixel((y, x), (0, 0, 0))
        file_name = os.path.basename(file)
        try:
            image2.save(f"{destination_folder}/{file_name}")
        except (KeyError, OSError):
            image2 = image2.convert("RGB")
            image2.save(f"{destination_folder}/{file_name}")


if __name__ == "__main__":
    process_images("captcha_processing/preprocessing/bdcaptcha")
