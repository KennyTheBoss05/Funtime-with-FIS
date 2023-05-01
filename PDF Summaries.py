# importing required modules
import PyPDF2
from transformers import TFPegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline
model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = TFPegasusForConditionalGeneration.from_pretrained(model_name,from_tf=True)
summarizer = pipeline("summarization",model = model_name,tokenizer = pegasus_tokenizer,framework = "pt")

temp = ""
result = []
cname = "Tesla" #Enter company name as given in the database after scraping
year = "2020" #Enter the year (Need to purchase to get latest report)
option = 1 #0 for responsibility report and 1 for annual report
if option==1:
    rep = "AnnualReport"
else:
    rep = "ResponsibilityReport"
filename = cname+rep+year+".pdf"
# creating a pdf file object
pdfFileObj = open(filename, 'rb') #Put the report name

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
n = pdfReader.numPages
print(pdfReader.numPages)

for i in range (3,n):
    # creating a page object
    pageObj = pdfReader.getPage(i)
    # extracting text from page
    #print(pageObj.extractText())
    temp = pageObj.extractText()
    result.append(temp.split('\n'))#The resultant list consists of lists of each line of a page
    break
    #Run each line into the zero shot model

# closing the pdf file object
pdfFileObj.close()
#print(result)

Result = []
tempo = []
for i in result:
    for j in i:
        hmm = str(j).replace('\t',' ')
        tempo.append(hmm)
    Result.append(tempo)
    tempo = []

#print (Result)
#print(len(result[0]))
tempstr = ""
pages = []
for i in Result:
    for j in i:
        tempstr = tempstr + " " + str(j)
    pages.append(tempstr)
    tempstr = ""

print (pages)
summaries = []
for p in pages:
    summary = summarizer(p,min_length = 30,max_length = 100)
    summaries.append(summary)

print(summaries)

