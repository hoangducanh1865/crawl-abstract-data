import requests
from bs4 import BeautifulSoup


url = 'https://vjol.info.vn/plugins/generic/pdfJsViewer/pdf.js/web/viewer.html?file=https%3A%2F%2Fvjol.info.vn%2Findex.php%2Fkhcn%2Farticle%2Fdownload%2F74277%2F63109%2F'
pdf_response = requests.get(url, verify=False)
file_name = 'input'

with open('./pdf/' + file_name, 'wb') as f:
    f.write(pdf_response.content)
