import PyPDF2
import re
import mysql.connector


pdfFileObj = open('./data/csnt95-2022.pdf', 'rb')
  
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  
# printing number of pages in pdf file
print(pdfReader.numPages)
numPages = pdfReader.numPages
# creating a page object
# pageObj = pdfReader.getPage(0)
# pageObj2 = pdfReader.getPage(1)

# data = pageObj.extractText()
# data2 = pageObj2.extractText()
# splittedData = data.split() 
# splittedData2 = data2.split() 

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="test"
# )
# mycursor = mydb.cursor()

# sql = "INSERT INTO currency_data (currency, import_price, export_price) VALUES (%s, %s, %s)"
combined = [] #splittedData #+ splittedData2
if numPages > 0 : 
   j=0
   while j < numPages:
      pageObj = pdfReader.getPage(j)
      data = pageObj.extractText()
      splittedData = data.split()
      combined += splittedData
      j +=1
   #print(combined)
   regexDigit = re.compile(r'^\d*\.')
   i=0
   count = 1
   while i < len(combined):
      data = combined[i]
      # increment=5
      import_price=''
      export_price=''
      saveFlag=False
      if(regexDigit.match(combined[i]) and data[len(data)-1]=='.'):
         printData = str(count) + ': ' + combined[i+1] + ' '
         currency = combined[i+1] + ' '
         if len(combined) > (i+3) and regexDigit.match(combined[i+2]):
            printData += ' Import : ' + combined[i+2] + ' Export : ' + combined[i+3] 
            import_price = combined[i+2]
            export_price = combined[i+3] if float(combined[i+3]) > 0 else combined[i+4]
            saveFlag=True
         elif len(combined) > (i+4) and not(regexDigit.match(combined[i+2])) and regexDigit.match(combined[i+3]):
            printData += combined[i+2] + ' Import : ' + combined[i+3] + ' Export : ' + combined[i+4]
            currency += combined[i+2]
            import_price = combined[i+3]
            export_price = combined[i+4] if float(combined[i+4]) > 0 else combined[i+5]
            saveFlag=True
         elif len(combined) > (i+5) and  regexDigit.match(combined[i+4]):
            currency += combined[i+2] + ' ' + combined[i+3]
            import_price = combined[i+4]
            export_price = combined[i+5] #if float(combined[i+5]) > 0 else combined[i+6]
            printData = str(count) + ': ' + currency + ' Import : ' + combined[i+4] + ' Export : ' + combined[i+5]
            increment = 6
            saveFlag=True

         if saveFlag:
            print(printData)
            count+=1
         # if len(import_price) > 0 and len(export_price) > 0 :
         #    val = (currency, import_price, export_price)
         #    mycursor.execute(sql, val)
         #    mydb.commit()
         i+=1
      else:
         i+=1
      

# closing the pdf file object
pdfFileObj.close()