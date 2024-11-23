import os

import cv2
import glob


os.makedirs("captcha_processing/preprocessing/letters", exist_ok=True)
os.makedirs("captcha_processing/preprocessing/identified", exist_ok=True)

files = glob.glob("captcha_processing/preprocessing/processed/*")
for file in files:
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, new_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)

    # Filtering letters contours
    contours, _ = cv2.findContours(new_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    letters_contours = []
    for contour in contours:
        (x, y, width, height) = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > 115:
            letters_contours.append((x, y, width, height))

    if len(letters_contours) != 5:
        continue

    # Drawing letters and storing individually
    final_image = cv2.merge([image] * 3)
    i = 0
    for rectangle in letters_contours:
        x, y, width, height = rectangle
        letter_image = image[y - 2: y + height + 2, x - 2: x + width + 2]
        if letter_image.size == 0:
            continue

        i += 1
        file_name = os.path.basename(file).replace(".png", f"letter{i}.png")
        cv2.imwrite(f"captcha_processing/preprocessing/letters/{file_name}", letter_image)
        cv2.rectangle(final_image, (x-2, y-2), (x+width+2, y+height+2), (0, 255, 0), 1)

    file_name = os.path.basename(file)
    cv2.imwrite(f"captcha_processing/preprocessing/identified/{file_name}", final_image)
