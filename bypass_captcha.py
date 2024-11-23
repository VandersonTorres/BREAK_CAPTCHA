import cv2
import pickle
import numpy as np
from keras.api.models import load_model
from helpers import resize_to_fit
from imutils import paths

from process_captcha import process_images


def bypass_captcha():
    # Get the trained model and the model_labels
    with open("model_labels.dat", "rb") as translater_file:
        lb = pickle.load(translater_file)

    model = load_model("trained_model.hdf5")

    # USING THE MODEL

    # Read the files in /to_solve and handle each img with characters
    process_images(origin_folder="to_solve", destination_folder="to_solve")

    files = list(paths.list_images("to_solve"))
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

        letters_contours = sorted(letters_contours, key=lambda x: x[0])

        predictions = []
        for rectangle in letters_contours:
            x, y, width, height = rectangle
            letter_image = image[y - 2: y + height + 2, x - 2: x + width + 2]
            if letter_image.size == 0:
                continue

            letter_image = resize_to_fit(letter_image, 20, 20)
            letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = np.expand_dims(letter_image, axis=0)

            predicted_letter = model.predict(letter_image)
            predicted_letter = lb.inverse_transform(predicted_letter)[0]
            predictions.append(predicted_letter)

        prediction_text = "".join(predictions)
        print(prediction_text)  # RESULT
        return prediction_text


if __name__ == "__main__":
    bypass_captcha()