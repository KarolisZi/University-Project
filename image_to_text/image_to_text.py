import pytesseract
from PIL import Image

absolute_path = 'C:/Users/kikar.LAPTOP-Q25785DG/OneDrive/Desktop/University-Project/images/'
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\kikar.LAPTOP-Q25785DG\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def convert(topic_id, len_images):
    results = []

    for i in range(0, len_images):
        name = str(topic_id) + "_" + str(i) + ".png"
        image_path = absolute_path + name
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            results.append(text)
        except FileNotFoundError as error:
            print('The picture %s has not been found for conversion to text: ' % name, error)

    return results
