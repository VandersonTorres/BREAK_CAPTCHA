import cv2
from PIL import Image

methods = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV
]

image = cv2.imread("bdcaptcha/telanova0.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
_, processed_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
cv2.imwrite("tests_methods/processed_image.png", processed_image)

image = Image.open("tests_methods/processed_image.png")
image = image.convert("P")
image2 = Image.new("P", image.size, (255, 255, 255))
for x in range(image.size[1]):
    for y in range(image.size[0]):
        pixel_color = image.getpixel((y, x))
        if pixel_color < 115:
            image2.putpixel((y, x), (0, 0, 0))
image2.save("tests_methods/final_image.png")
