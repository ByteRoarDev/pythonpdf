from pdf2image import convert_from_path
pdfs = r"./data/csnt93-2022.pdf"
pages = convert_from_path(pdfs, 350)

i = 1
for page in pages:
   image_name = "Page_" + str(i) + ".jpg"  
   page.save(image_name, "JPEG")
   i = i+1