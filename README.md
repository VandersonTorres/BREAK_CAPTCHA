# BREAK_CAPTCHA
Trained Large Language Model based on Convolutional Neural Networks to identify letters through captcha images and solve them automatically.

## Directories Overview
1. `/captcha_processing`: Is a directory destinated to handle and process captcha images, in addition to train a LLM

    - `/captcha_processing/preprocessing`: Contains the images that will be tested. These images are structured in subdirs and the following is mandatory being implemented: 
    `/bdcaptcha`: The only one that is mandatory and must contains a lot of captcha images for being tested and processed later.

    - `/captcha_processing/tests_methods`: Contains a base script to test the general processing of image treatment.

    - `/captcha_processing/model_training`:

    1. 'process_captcha.py' makes initial processing in each image on `/bdcaptcha`. 

    2. 'separate_letters.py' breaks the captcha by letter and marks them.

    3. 'train_model.py' trains the LLM to recognize any image based on the previous processing, finally storing the `trained_model`.

    - `/captcha_processing/trained_model`: Contains the labels and the trained model, and finally a script that bypass a regular captcha

2. `/web_automation`: Is a directory destinated to access the website '2captcha' (workers mode) and integrate the generated captchas to BREAK_CAPTCHA bot

## CONCLUSION

The main idea is Access "2captcha.com", logging in, sending the generated captchas to the bot, solve them, and finally submit by filling the form with the result.
