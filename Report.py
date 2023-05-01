# Import libraries
import requests
from bs4 import BeautifulSoup
import PyPDF2
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline
model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name,from_tf=True)
summarizer = pipeline("summarization",model = model_name,tokenizer = pegasus_tokenizer,framework = "pt")

def getpages(company,y):

    temp = ""
    annualresult = []
    responsibilityresult = []
    s= ""
    # URL from which pdfs to be downloaded
    #url = "https://www.geeksforgeeks.org/how-to-extract-pdf-tables-in-python/"
    cname = company #Enter company name here
    needyear = y
    url = "https://www.annualreports.com/Companies?search="+cname
    response = requests.get(url)

    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if ('/Company' in str(link.get('href', []))):
            s = str(link.get('href', []))[9:]
            break
    #print(s)

    if s != "":
        url = "https://www.annualreports.com/Company/"+s
        url2 = "https://www.responsibilityreports.com/Company/"+s
        # Requests URL and get response object
        #print("Getting annual reports")
        response = requests.get(url)

        # Parse text obtained
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all hyperlinks present on webpage
        links = soup.find_all('a')

        i = 0
        # From all links check for pdf link and
        # if present download file
        for link in links:
            if ('.pdf' in str(link.get('href', [])) and 'title' in str(link)):
                i += 1
                #print("Downloading file: ", i)

                # Get response object for link
                year = str(link.get('href'))[len(str(link.get('href')))-8:len(str(link.get('href')))-4]
                if year == needyear:
                    response = requests.get("https://www.annualreports.com/" + link.get('href'))

                    # Write content in pdf file
                    pdf = open(cname + "AnnualReport" + year + ".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()
                    """
                    #print("File ", i, " downloaded")
                    filename = cname + "AnnualReport" + year + ".pdf"
                    # creating a pdf file object
                    pdfFileObj = open(filename, 'rb')  # Put the report name
    
                    # creating a pdf reader object
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
                    # printing number of pages in pdf file
                    n = pdfReader.numPages
                    #print(pdfReader.numPages)
    
                    for i in range(0, n):
                        # creating a page object
                        pageObj = pdfReader.getPage(i)
                        # extracting text from page
                        # print(pageObj.extractText())
                        temp = pageObj.extractText()
                        annualresult.append(temp.split('\n'))  # The resultant list consists of lists of each line of a page
                        # Run each line into the zero shot model
    
                    # closing the pdf file object
                    pdfFileObj.close()
                    """

        #print("Getting responsibility reports")
        response = requests.get(url2)

        # Parse text obtained
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all hyperlinks present on webpage
        links = soup.find_all('a')

        i = 0
        # From all links check for pdf link and
        # if present download file
        for link in links:
            if ('.pdf' in str(link.get('href', [])) and 'title' in str(link)):
                i += 1
                #print("Downloading file: ", i)

                # Get response object for link
                #response = requests.get("https://www.responsibilityreports.com/"+link.get('href'))
                year = str(link.get('href'))[len(str(link.get('href'))) - 8:len(str(link.get('href'))) - 4]
                if year == needyear:
                    response = requests.get("https://www.responsibilityreports.com/" + link.get('href'))

                    # Write content in pdf file
                    pdf = open(cname + "ResponsibilityReport" + year + ".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()
                    """
                    #print("File ", i, " downloaded")
                    filename = cname + "ResponsibilityReport" + year + ".pdf"
                    # creating a pdf file object
                    pdfFileObj = open(filename, 'rb')  # Put the report name
    
                    # creating a pdf reader object
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
                    # printing number of pages in pdf file
                    n = pdfReader.numPages
                    # print(pdfReader.numPages)
    
                    for i in range(0, n):
                        # creating a page object
                        pageObj = pdfReader.getPage(i)
                        # extracting text from page
                        # print(pageObj.extractText())
                        temp = pageObj.extractText()
                        responsibilityresult.append(temp.split('\n'))  # The resultant list consists of lists of each line of a page
                        # Run each line into the zero shot model
    
                    # closing the pdf file object
                    pdfFileObj.close()
    
        #print("All PDF files downloaded")
        #print(annualresult)
        #print("------------------------------------")
        #print(responsibilityresult)
        """
        return 1
    else:
        return 0


def getsummaries(company,y,op):
    temp = ""
    result = []
    cname = company  # Enter company name as given in the database after scraping
    year = y  # Enter the year (Need to purchase to get latest report)
    option = op  # 0 for responsibility report and 1 for annual report
    if option == 1:
        rep = "AnnualReport"
    else:
        rep = "ResponsibilityReport"
    filename = cname + rep + year + ".pdf"
    # creating a pdf file object
    pdfFileObj = open(filename, 'rb')  # Put the report name

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    n = pdfReader.numPages
    print(pdfReader.numPages)

    for i in range(0, n):
        # creating a page object
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        # print(pageObj.extractText())
        temp = pageObj.extractText()
        result.append(temp.split('\n'))  # The resultant list consists of lists of each line of a page
        # Run each line into the zero shot model

    # closing the pdf file object
    pdfFileObj.close()
    # print(result)

    Result = []
    tempo = []
    for i in result:
        for j in i:
            hmm = str(j).replace('\t', ' ')
            tempo.append(hmm)
        Result.append(tempo)
        tempo = []

    # print (Result)
    # print(len(result[0]))
    tempstr = ""
    pages = []
    for i in Result:
        for j in i:
            tempstr = tempstr + " " + str(j)
        pages.append(tempstr)
        tempstr = ""

    #print(pages)
    summaries = []
    for p in pages:
        summary = summarizer(p, min_length=30, max_length=100)
        summaries.append(summary)

    return summaries


if __name__ == "__main__":
    annualsummary = []
    responsibilitysummary = []
    check = 0
    companyname = "Tesla"
    cyear = 2020
    check = getpages(companyname,cyear) #Downloads the annual and responsibility report of that company for that year and returns whether
    # company is found in database or not
    if check==1:
        annualsummary = getsummaries(companyname,cyear,1) #Gets summaries of annual report
        responsibilitysummary = getsummaries(companyname, cyear, 2) #Gets summaries of responsibility report
    else:
        print("Company data doesn't exist")