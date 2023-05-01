# Import libraries
import requests
from bs4 import BeautifulSoup

s= ""
# URL from which pdfs to be downloaded
#url = "https://www.geeksforgeeks.org/how-to-extract-pdf-tables-in-python/"
cname = "Tesla" #Enter company name here

url = "https://www.annualreports.com/Companies?search="+cname
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
for link in links:
    if ('/Company' in str(link.get('href', []))):
        s = str(link.get('href', []))[9:]
        break
print(s)

if s != "":
    url = "https://www.annualreports.com/Company/"+s
    url2 = "https://www.responsibilityreports.com/Company/"+s
    # Requests URL and get response object
    print("Getting annual reports")
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
            print("Downloading file: ", i)

            # Get response object for link
            response = requests.get("https://www.annualreports.com/"+link.get('href'))
            year = str(link.get('href'))[len(str(link.get('href')))-8:len(str(link.get('href')))-4]

            # Write content in pdf file
            pdf = open(cname + "AnnualReport" + year + ".pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")

    print("Getting responsibility reports")
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
            print("Downloading file: ", i)

            # Get response object for link
            response = requests.get("https://www.responsibilityreports.com/"+link.get('href'))
            year = str(link.get('href'))[len(str(link.get('href'))) - 8:len(str(link.get('href'))) - 4]

            # Write content in pdf file
            pdf = open(cname + "ResponsibilityReport" + year + ".pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")

    print("All PDF files downloaded")
else:
    print("Company not found in database")