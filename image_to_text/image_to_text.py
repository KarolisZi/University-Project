import pytesseract
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True

absolute_path = 'C:/Users/kikar.LAPTOP-Q25785DG/OneDrive/Desktop/University-Project/images/'
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\kikar.LAPTOP-Q25785DG\OneDrive\Desktop\University-Project\Tesseract-OCR\tesseract.exe"


def convert(topic_id, image_id):
    name = str(topic_id) + "_" + str(image_id) + ".png"
    image_path = absolute_path + name

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
    except FileNotFoundError as error:
        print('The picture %s has not been found for conversion to text: ' % name, error)

    return text
