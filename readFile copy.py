import PyPDF2
import re
import mysql.connector

pdfFileObj = open('../data/csnt90.pdf', 'rb')
  
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  
# printing number of pages in pdf file
print(pdfReader.numPages)
  
# creating a page object
pageObj = pdfReader.getPage(0)
pageObj2 = pdfReader.getPage(1)

data = pageObj.extractText()
data2 = pageObj2.extractText()
splittedData = data.split() 
splittedData2 = data2.split() 

# status = 0
# i = 0
# while i < len(splittedData):
#    increment = 5
#    if splittedData[i] == '1.':
#       printData = splittedData[i+1] + ' ' + splittedData[i+2] + ' => Import : ' + splittedData[i+3] + ' Export : ' + splittedData[i+4]
#       if splittedData[i+5] == '0':
#          printData+=splittedData[i+5]
#          increment=6
#       print(printData)
#       print('---------------------------------------------------')
#       status=1
#       i += increment
#    elif(status == 1 and ((i+4) < len(splittedData))):
#       if(splittedData[i+1] == 'EURO'):
#          printData = splittedData[i+1] + ' => Import : ' + splittedData[i+2] + ' Export : ' + splittedData[i+3]
#          increment=4
#       elif(splittedData[i+1] == 'New' or splittedData[i+1] == 'Hong'):
#          printData = splittedData[i+1] + ' ' + splittedData[i+2] + ' ' + splittedData[i+3] +' => Import : ' + splittedData[i+4] + ' Export : ' + splittedData[i+5]
#          increment=6
#       else:
#          printData = splittedData[i+1] + ' ' + splittedData[i+2] +' => Import : ' + splittedData[i+3] + ' Export : ' + splittedData[i+4]
#       if (i+5) < len(splittedData) and splittedData[i+5] == '0':
#          printData+=splittedData[i+5]
#          increment=increment+1

#       print(printData)
#       print('---------------------------------------------------')
#       i += increment
#    else:
#       i+=1

# status = 0
# i = 0 
# while i < len(splittedData2):
#    increment = 5
#    if(splittedData2[i] == 'SCHEDULE'):
#       break
#    if splittedData2[i] == '11.':
#       printData = splittedData2[i+1] + ' ' + splittedData2[i+2] + ' => Import : ' + splittedData2[i+3] + ' Export : ' + splittedData2[i+4]
#       if splittedData2[i+5] == '0':
#          printData+=splittedData2[i+5]
#          increment=6
#       print(printData)
#       print('---------------------------------------------------')
#       status=1
#       i += increment
#    elif(status == 1 and ((i+4) < len(splittedData2))):
#       if(splittedData2[i+1] == 'South' or splittedData2[i+1] == 'Saudi'):
#          printData = splittedData2[i+1] + ' ' + splittedData2[i+2] + ' ' + splittedData2[i+3] +' => Import : ' + splittedData2[i+4] + ' Export : ' + splittedData2[i+5]
#          increment=6
#       else:
#          printData = splittedData2[i+1] + ' ' + splittedData2[i+2] +' => Import : ' + splittedData2[i+3] + ' Export : ' + splittedData2[i+4]
#       if (i+5) < len(splittedData2) and splittedData2[i+5] == '0':
#          printData+=splittedData2[i+5]
#          increment=increment+1

#       print(printData)
#       print('---------------------------------------------------')
#       i += increment
#    else:
#       i+=1




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="test"
)
mycursor = mydb.cursor()

sql = "INSERT INTO currency_data (currency, import_price, export_price) VALUES (%s, %s, %s)"
combined = splittedData + splittedData2
regexDigit = re.compile(r'^\d*\.')
i=0
while i < len(combined):
   data = combined[i]
   increment=5
   if(regexDigit.match(combined[i]) and data[len(data)-1]=='.'):
      printData = combined[i+1] + ' '
      currency = combined[i+1] + ' '
      if regexDigit.match(combined[i+2]):
         printData += ' Import : ' + combined[i+2] + ' Export : ' + combined[i+3] 
         import_price = combined[i+2]
         export_price = combined[i+3] if float(combined[i+3]) > 0 else combined[i+4]
      elif not(regexDigit.match(combined[i+2])) and regexDigit.match(combined[i+3]):
         printData += combined[i+2] + ' Import : ' + combined[i+3] + ' Export : ' + combined[i+4]
         currency += combined[i+2]
         import_price = combined[i+3]
         export_price = combined[i+4] if float(combined[i+4]) > 0 else combined[i+5]
      else:
         currency += combined[i+2] + ' ' + combined[i+3]
         import_price = combined[i+4]
         export_price = combined[i+5] if float(combined[i+5]) > 0 else combined[i+6]
         printData = currency + ' Import : ' + combined[i+4] + ' Export : ' + combined[i+5]
         increment = 6
      print(printData)
      val = (currency, import_price, export_price)
      mycursor.execute(sql, val)
      mydb.commit()
      i+=increment
   else:
      i+=1
   

# closing the pdf file object
pdfFileObj.close()