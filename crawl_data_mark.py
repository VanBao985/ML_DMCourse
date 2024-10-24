import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
#Tranh bi chan truy cap
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def crawl_mark(so_bao_danh):
    so_bao_danh = str(so_bao_danh).rjust(8, '0')
    URL = "https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{}.html".format(so_bao_danh)
    r = session.get(URL)
    if r.status_code != 404:
        soup = BeautifulSoup(r.content, 'html.parser')
        target = soup.find('div', attrs={'class': 'resultSearch__right'})
        table = target.find('tbody')
        rows = table.find_all('tr')
        placeHolder = []
        for row in rows:
            lst = row.find_all('td')
            cols = [ele.text.strip() for ele in lst]
            placeHolder.append([ele for ele in cols if ele])
        return placeHolder
    else:
        return None

# Xu ly format diem de luu vao file csv:
finally_dict = {'sbd':[], 'Toán':[], 'Văn':[], "Lí":[], 'Hóa':[], 'Sinh':[], "Ngoại ngữ":[], "Sử":[], "Địa":[], "GDCD":[]}
all_subjects = ('Toán', 'Văn', "Lí", 'Hóa', 'Sinh', "Ngoại ngữ", "Sử", "Địa", "GDCD")
def processing_mark(marks):
    global finally_dict
    for student in marks:
        subject_dict = {sub[0]: float(sub[1]) for sub in student} 
        for subject in all_subjects:
            if subject in subject_dict:
                finally_dict[subject].append(subject_dict[subject])
            else:
                finally_dict[subject].append(None) 
            
sbd = []
marks = []
#crawl data: 30.000 thí sinh Hà Nội 
start = 1030001
for x in tqdm(range(start, start+5)):
    cnt = 0
    sub = crawl_mark(str(x).rjust(8, '0'))
    if sub != None:
        sbd.append(x)
        marks.append(sub)
    else:
        cnt+=1
        if cnt==10:
            break

finally_dict['sbd']=sbd
processing_mark(marks)
data = pd.DataFrame(finally_dict)
# # data.to_csv("./data/xx.csv", index=None)
# with open("./data/mark.csv","a") as f:
#     data.to_csv(f,header=False,index=False)