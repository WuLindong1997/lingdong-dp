import time
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import re
import os
import multiprocessing
from PIL import Image

def is_dir_empty(path):
    return len(os.listdir(path)) == 0
def getHTMLText(url):
    root_path = 'https://www.shijuan1.com'
    """爬虫通用代码框架"""
    result = []
    #首先给访问的一个身份标识
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Charset": "gb2312"
    }
    end_url = url
    request = requests.get(end_url, headers=headers, stream=True, verify=False)
    if request.status_code != 200:
        print(f"{end_url}:{request.status_code}")
    request.encoding = "gb2312"
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    soups = soup.find_all('span', attrs={'class': 'more'})
    intros = [(a_item.find('a').get('href'),a_item.find('a').get('title')) for a_item in soups if a_item.find('a').get('title')!=None]
    pass
    for subset_path,foldername in intros:
        
        time.sleep(0.3)
        try:

            headers1 = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            }
            time.sleep(0.3)
            pattern = r'\d{5,}'

            # 查找所有符合条件的匹配项
            id = re.findall(pattern, subset_path)[0]
            
            requeset_path = "https://www.zxxk.com/soft/Preview/FirstLoadPreviewJson"
            params = {
                'softID': id,
                'fileaddress': '',
                'type': '3',
                'FullPreview': 'true'
            }
            request_subset = requests.get(requeset_path, headers=headers1,params= params).json()
            
            request_subset = request_subset['data']['Html']

            soup_subset = BeautifulSoup(request_subset, 'html.parser')
            soup_subset = soup_subset.find_all('img')
            imgs_url = [img_url.get('data-original') for img_url in soup_subset]
            
            
            
            if not os.path.exists(os.path.join(root_path,foldername)):
                os.makedirs(os.path.join(root_path,foldername))
                print(f'The folder {foldername} has been created.')
            else:
                print(f'The folder {foldername} already exists.')
                continue
            count= 0
            for img_url in imgs_url:
                time.sleep(0.1)
                img_response = requests.get(img_url, headers=headers1)
                save_path = os.path.join(root_path,foldername,id+f'_{count}'+'.PNG')
                count+=1
                # 保存响应内容到本地文件
                # with open(save_path, 'wb') as f:
                try:
                    image = Image.open(BytesIO(img_response.content))
                    image.save(save_path)
                except:
                    image_soup = BeautifulSoup(img_response, 'html.parser')
                    image = Image.open(BytesIO(image_soup.find('image').get('xlink:href')))
                    image.save(save_path)
                    
                
            if is_dir_empty(os.path.join(root_path,foldername)):
                result.append(subset_path+foldername+'\t'+"False")
            else:
                result.append(subset_path+foldername+'\t'+"True")    
        except:
            
            print(subset_path)

    #然后对每个链接进行get请求

    # intros = [re.sub(r'\[\d+(?:-\d+)?\]', '', intro) for intro in intros]  # 去掉引用符号
    with open('/mnt/vepfs/Pretrain-data/wulindong/safety_data/xkw/ddyfz/result.txt','w',encoding='utf-8')as file:
        file.write('\n'.join(result))


if __name__ == '__main__':
    

    text = getHTMLText('https://www.shijuan1.com/a/sjzz/')
    pass