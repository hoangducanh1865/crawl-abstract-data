import re
import requests
import urllib3
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

tieng_viet = [
    'á', 'à', 'ả', 'ã', 'ạ',
    'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ',
    'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
    'đ',
    'é', 'è', 'ẻ', 'ẽ', 'ẹ',
    'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
    'í', 'ì', 'ỉ', 'ĩ', 'ị',
    'ó', 'ò', 'ỏ', 'õ', 'ọ',
    'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ',
    'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
    'ú', 'ù', 'ủ', 'ũ', 'ụ',
    'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
    'Á', 'À', 'Ả', 'Ã', 'Ạ',
    'Ă', 'Ắ', 'Ằ', 'Ẳ', 'Ẵ', 'Ặ',
    'Â', 'Ấ', 'Ầ', 'Ẩ', 'Ẫ', 'Ậ',
    'Đ',
    'É', 'È', 'Ẻ', 'Ẽ', 'Ẹ',
    'Ê', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ',
    'Í', 'Ì', 'Ỉ', 'Ĩ', 'Ị',
    'Ó', 'Ò', 'Ỏ', 'Õ', 'Ọ',
    'Ô', 'Ố', 'Ồ', 'Ổ', 'Ỗ', 'Ộ',
    'Ơ', 'Ớ', 'Ờ', 'Ở', 'Ỡ', 'Ợ',
    'Ú', 'Ù', 'Ủ', 'Ũ', 'Ụ'
    'Ư', 'Ứ', 'Ừ', 'Ử', 'Ữ', 'Ự'
]

keywords_to_skip = ['English', 'Tiếng Anh', '2025', '2024', '2023']



def check_name(s):
    for c in s:
        if c in tieng_viet: 
            return False # La tieng Viet
    return True # La tieng Anh

source_url = 'https://vjol.info.vn/'
source_response = requests.get(source_url, verify=False)
source_content = BeautifulSoup(source_response.text, 'lxml')
all_source_urls = source_content.find_all('a')
base_pre_pre_urls = []
count = 0
for url in all_source_urls:
    
    href = url.get('href')
    if url.find('img'):
        count += 1
        if count >= 1: base_pre_pre_urls.append(href)
        if count >= 3:
            break
        # print('*********', href)
base_pre_pre_urls.pop(0)
# base_pre_pre_urls.pop()
for urrl in base_pre_pre_urls:
    print(urrl)
print('*')
print(len(base_pre_pre_urls))

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
print('**')
print(len(pre_pre_pdf_urls))

pre_pdf_urls = []
for pre_pre_pdf_url in pre_pre_pdf_urls:
    response = requests.get(pre_pre_pdf_url, verify=False)
    content = BeautifulSoup(response.text, 'lxml')
    all_urls = content.find_all('a')

    for url in all_urls:
        try:
            href = url['href']
            if pre_pre_pdf_url[-1] == 'e':
                keychain = pre_pre_pdf_url.replace('archive', 'view')
            else:
                keychain = pre_pre_pdf_url.replace(r'archive/\d+', 'view')
            
            if keychain in href: # Co truong hop href bi lap, co truong hop thi khong
                if any(keyword in url.text for keyword in keywords_to_skip) or check_name(url.text):
                    if len(pre_pdf_urls) != 0 and href == pre_pdf_urls[-1]:
                        pre_pdf_urls.pop()
                    continue
                if len(pre_pdf_urls) != 0 and href == pre_pdf_urls[-1]: 
                    continue 
                pre_pdf_urls.append(href)
                
        except Exception as e:
            print("Error: ", e)
             
# print(pre_pdf_urls)
print('***')
print(len(pre_pdf_urls))

pdf_urls = []
for pre_pdf_url in pre_pdf_urls:
    response = requests.get(pre_pdf_url, verify=False)
    content = BeautifulSoup(response.text, 'lxml')
    all_urls = content.find_all('a')

    for url in all_urls:
        href = url['href']
        try:
            keychain = pre_pdf_url.replace('issue', 'article')
            keychain = re.sub(r'/\d+$', '', keychain)
            # print('***', keychain) 
            
            if re.match(re.escape(keychain) + r'/\d+/\d+$', href):
                pdf_url = href.replace('view', 'download') 
                if 'English' in url.text or 'Tiếng Anh' in url.text:
                    if len(pdf_urls) != 0 and href == pdf_urls[-1]:
                        pdf_urls.pop()
                    continue
                if len(pdf_urls) != 0 and pdf_url == pdf_urls[-1]:
                    continue
                pdf_urls.append(pdf_url)

        except Exception as e:
            print("Error: ", e)
            
# print(pdf_urls)
print('****')
print(len(pdf_urls))
            
count = 0
for pdf_url in pdf_urls:
    try:
        pdf_response = requests.get(pdf_url, verify=False)
        count += 1
        file_name = "input" + str(count) + '.pdf'
        
        with open('/Users/hoangducanh/Documents/Hoc o HUST/nhom_anh_minh/crawl-abstract-data/data/' + file_name, 'wb') as f:
            f.write(pdf_response.content)
            print("✅ Input {} is written into pdf folder successfully!".format(count))
    except Exception as e:
            print("Error: ", e)