import PyPDF2
 
#create file object variable
#opening method will be rb
pdffileobj=open('demo.pdf','rb')
 
#create reader variable that will read the pdffileobj
pdfreader=PyPDF2.PdfFileReader(pdffileobj)
 
#This will store the number of pages of this pdf file
x=pdfreader.numPages
 
#create a variable that will select the selected number of pages
# pageobj=pdfreader.getPage(x-1)

file1=open(r"out.txt","a")
for i in range(x):
    pageobj=pdfreader.getPage(i)
    text=pageobj.extractText()
    file1.writelines(text)