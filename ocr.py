from PIL import Image as img
import pytesseract as PT
from pdf2image import convert_from_path as CFP

# Importing the pdf file
PDF_file_1 = "./data/csnt97-2022.pdf"
pages_1 = CFP(PDF_file_1, 9)
image_counter1 = 1

# Iterating through all the pages of the pdf file stored above
for page in pages_1:
   filename1 = "Page_no_" + str(image_counter1) + " .jpg"
   page.save(filename1, 'JPEG')
   image_counter1 = image_counter1 + 1


filelimit1 = image_counter1 - 1
out_file1 = "output_text.txt"
f_1 = open(out_file1, "a")

    # Iterating from 1 to total number of pages
for K in range(1, filelimit1 + 1):
   filename1 = "Page_no_" + str(K) + " .jpg"
   text1 = str(((PT.image_to_string(img.open(filename1)))))
   text1 = text1.replace('-\n', '')
   f_1.write(text1)

f_1.close()
