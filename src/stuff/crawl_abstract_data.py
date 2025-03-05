import re
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


keywords = ['khcn', 'dh-NTT']

base_pre_pre_urls = []

for keyword in keywords:
    url = 'https://vjol.info.vn/index.php/' + keyword + '/issue/archive'
    base_pre_pre_urls.append(url)
    
pre_pre_pdf_urls = []
    
for base_pre_pre_url in base_pre_pre_urls:
    pre_pre_pdf_urls.append(base_pre_pre_url) # Them trang dau tien vao list

    count = 2
    pre_pre_pdf_url = base_pre_pre_url + '/' + str(count)
    response = requests.get(pre_pre_pdf_url, verify=False)
    content = BeautifulSoup(response.text, 'lxml')

    while 'Kế tiếp' in content.text:
        pre_pre_pdf_urls.append(pre_pre_pdf_url)
        count += 1
        pre_pre_pdf_url = base_pre_pre_url + '/' + str(count)
        response = requests.get(pre_pre_pdf_url, verify=False)
        content = BeautifulSoup(response.text, 'lxml')
        
    pre_pre_pdf_urls.append(pre_pre_pdf_url)  # Them trang cuoi cung vao list

# print(pre_pre_pdf_urls)

pre_pdf_urls = []

for pre_pre_pdf_url in pre_pre_pdf_urls:
    response = requests.get(pre_pre_pdf_url, verify=False)
    content = BeautifulSoup(response.text, 'lxml')
    all_urls = content.find_all('a')


    count = 0
    for url in all_urls:
        try:
            href = url['href']
            # if 'https://vjol.info.vn/index.php/khcn/issue/view/' in href: # Co truong hop href bi lap, co truong hop thi khong
            #     pre_pdf_urls.append(href)
            if pre_pre_pdf_url[-1] == 'e':
                keychain = pre_pre_pdf_url.replace('archive', 'view')
            else:
                keychain = pre_pre_pdf_url.replace(r'archive/\d+', 'view')
            
            if keychain in href: # Co truong hop href bi lap, co truong hop thi khong
                pre_pdf_urls.append(href)
                
        except Exception as e:
            print("Error: ", e)
            
# print(pre_pdf_urls)

count = 0
for pre_pdf_url in pre_pdf_urls:
    response = requests.get(pre_pdf_url, verify=False)
    content = BeautifulSoup(response.text, 'lxml')
    all_urls = content.find_all('a')

    for url in all_urls:
        try:
            keychain = pre_pdf_url.replace('issue', 'article')
            keychain = re.sub(r'/\d+$', '', keychain)
            # print('***', keychain)
            
            if re.match(re.escape(keychain) + r'/\d+/\d+$', url['href']):
                
                download_url = url['href'].replace('view', 'download')
                # print('*****', download_url)
                pdf_response = requests.get(download_url, verify=False)
                # print(url['href'])
                
                count += 1
                file_name = "input" + str(count) + '.pdf'
                
                with open('/Users/hoangducanh/Documents/Hoc o HUST/nhom_anh_minh/crawl-abstract-data/pdf/' + file_name, 'wb') as f:
                    f.write(pdf_response.content)
                    print("✅ Input {} is written into pdf folder successfully!".format(count))
        except Exception as e:
            print("Error: ", e)
            
         