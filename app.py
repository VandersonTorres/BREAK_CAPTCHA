from captcha_processing.trained_model.bypass_captcha import bypass_captcha

bypass_captcha()
# 1. GET THE CAPTCHA IMAGE;
# 2. STORE THE CAPTCHA IMG TO "/to_solve"
# 3. GET THE CAPTCHA TEXT RUNNING "bypass_captcha()"
# 4. FILL FORM WITH THE TEXT
# 5. SEND THE FORM
# 6. CHECK IF THE CAPTCHA WAS SUCCESSFULY SOLVED
# 6.1 IF YES, DELETE THE CAPTCHA IMAGE PREVIOUSLY STORED AND FOLLOW THE FLOW
# 6.2 IF NOT, CREATE A NEW FOLDER "failed", STORE THE CAPTCHA IMG, AND DELETE IT FROM CURRENT DIR, FINALLY FOLLOW THE FLOW
