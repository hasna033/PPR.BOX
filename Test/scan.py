from unittest import result
from pytesseract import pytesseract
import cv2

# Path to the location of the Tesseract-OCR executable/command
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def read_text_from_image(image):
  """Reads text from an image file and outputs found text to text file"""
  # Convert the image to grayscale
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Perform OTSU Threshold
  ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

  dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)

  _, contours, hierachy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  image_copy = image.copy()

  result = ""

  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)

    cropped = image_copy[y : y + h, x : x + w]

    file = open("results.txt", "a")

    text = pytesseract.image_to_string(cropped)

    result += text
    print(x, y, w, h, text)

    file.write(text)
    file.write("\n")

  file.close()
  return result

if __name__ == "__main__":

  image = cv2.imread("./images/input4.jpg")
  result = read_text_from_image(image)  
  print(result)