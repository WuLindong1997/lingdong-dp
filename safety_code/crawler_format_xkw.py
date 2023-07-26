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
    root_path = '/mnt/vepfs/Pretrain-data/wulindong/safety_data/xkw/体育与健康'
    """爬虫通用代码框架"""
    result = []
    for i in range(1,3):
        #首先给访问的一个身份标识
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Cookor":"xkw-device-id=1C89CCD0196F57C574292373C3DD8700; xk.school.schooluser=false; UT1=ut-105823-f3TYelcBUpw0pA; UT2=ut-105823-f3TYelcBUpw0pA; softCartList=; user-visitor-log=%7B%22firstTime%22%3A%222023-07-15T09%3A47%3A02.251Z%22%2C%22times%22%3A195%2C%22lastTime%22%3A%222023-07-19T06%3A07%3A19.297Z%22%7D; xk.passport.ticket=7532B0BD9F3A105CE692DD0E2BA3E9CE9877066FC14B8B30168929944B45652A2B05EC4EE71D86FD5A6E107346E44C05A4EE1EBBCB06663DA3F4543B3C50050DC4654E7B79855EF7A9D8E18C8D343C432F55F258CC183B69B42A935A977C680DF2798CC3AEA701B014308E166BFB76ED65EFCB2A55E80F61BEB72E57CC5C7CFFD9B2428A1D931AC2D419C0218DFB91AC994B426F1A4E0B30CB3A486B; xk.passport.ticket.v2=brnFXUcrrevaBjPUakBobgiYaT1+2dMEHW+fF/kDGKCdvjIDDtHm8MOzwAdD4S5r; xk.passport=8EBB293909AD2909A28072245BEBDDE589735D3BE5B0EE706A2AA1261EEE811AFD26728BCC79A6564ADE4B45D3F6B7614ACA9A29670F14CECB083516BA716E903935ECA42525FDABA18496ACE239209338124158B3D5DE622A79A7A6F300D9A1EECF830DBE3CB7903EF2E9DF10F25F99150B1BF790CEC6E3CB2383DBDAAC082D753938569D235534FFA91F5B8B0AAD8B432A86333B6D76CE6CA1D28E6C51A1BEAB66AEDAA96EFCEEDD87D9C97FA88C27146A41E1455457413550DF68139E0144CA5DC646B6126549AC1CF65E7D3220C66E2F56081CA7CF3B4D144C8D065A3BB7DDA7C61AA440F6DAB12BA607F2DAFBDC9DE7980D0FDBCD87354E25F49C65CF603E0D699D50A4B172C63B931FB568CA6523348767573FAB9F01772A0971D16E8152B0C6116CFACF43A770BE3A9126DD1417546A3F5893930CAADA8786E13BDD6467C8C06158E11A689ED74BF596E3C7D59C160FD399BAFFEF88780BF5ABE472766663643F; xk.passport.uid=71741349; xk.passport.info=%7b%22UserId%22%3a71741349%2c%22UserName%22%3a%22xkw_071741349%22%2c%22Identity%22%3a0%2c%22UserGroupID%22%3a4%2c%22SchoolId%22%3a0%2c%22endDataStr%22%3anull%2c%22Nick%22%3a%22xkw_071741349%22%2c%22userFace%22%3a%22https%3a%2f%2fzxxkstatic.zxxk.com%2fuc%2fimages%2fuserface%2f00001.jpg%22%2c%22RegTime%22%3a%222023-07-19+14%3a05%3a21%22%2c%22OrganNoticeUrl%22%3anull%2c%22OpenID%22%3anull%2c%22IsXiaoBen%22%3afalse%7d; xk.identity=%7b%7d; unread-message-num=10; userimage=%7b%22userid%22%3a71741349%2c%22mdm_subjectid%22%3a1%2c%22mdm_stageid%22%3a4%2c%22mdm_courseid%22%3a26%2c%22mdm_gradeid%22%3a0%2c%22mdm_versionid%22%3a0%2c%22mdm_textbookid%22%3a0%2c%22mdm_catalogid%22%3a0%2c%22mdm_pointid%22%3a0%2c%22mdm_provinceid%22%3a%22110000%22%2c%22economicid%22%3a0%2c%22updateTime%22%3anull%2c%22isSetting%22%3afalse%7d; site_history_search_kw=[%22%E5%BF%83%E7%90%86%E5%81%A5%E5%BA%B7%22%2C%22%E5%81%A5%E5%BA%B7%E6%88%90%E9%95%BF%22%2C%22%E5%81%A5%E5%BA%B7%E5%AE%89%E5%85%A8%22%2C%22%E5%81%A5%E5%BA%B7%E6%95%99%E8%82%B2%22%2C%22%E5%81%A5%E5%BA%B7%22%2C%22%E9%81%93%E5%BE%B7%E4%B8%8E%E6%B3%95%E6%B2%BB%22%2C%22%E7%A4%BC%E8%B2%8C%E6%96%87%E6%98%8E%22%2C%22%E7%A4%BC%E8%B2%8C%22%2C%22%E7%A4%BC%E8%B2%8C%E8%A1%A8%E8%BE%BE%22%2C%22%E6%96%87%E6%98%8E%22]; zxxk_latest_search_keyword=%E9%81%93%E5%BE%B7%E4%B8%8E%E6%B3%95%E6%B2%BB; lookedsoftstorage=[{%22softid%22:%2239999413%22}%2C{%22softid%22:%2240022643%22}%2C{%22softid%22:%2239979190%22}%2C{%22softid%22:%2239907781%22}%2C{%22softid%22:%2240023362%22}%2C{%22softid%22:%2238494730%22}%2C{%22softid%22:%2237986907%22}%2C{%22softid%22:%2233073086%22}%2C{%22softid%22:%2237303211%22}%2C{%22softid%22:%224815069%22}]; acw_tc=2f624a6d16897526179234238e2c6e2ff470306f72e756a16a5f8d765ad818; asyncLogin=1"
        }
        end_url = url.format(i)
        request = requests.get(end_url, headers=headers, stream=True, verify=False)
        if request.status_code != 200:
            print(f"{end_url}:{request.status_code}")
            continue
        
        html = request.text

        soup = BeautifulSoup(html, 'html.parser')
        soups = soup.find_all('div', attrs={'class': 'list-mid'})
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
    

    text = getHTMLText('https://search.zxxk.com/doc/type4105/index-{0}.html?free=1&kw=%e4%bd%93%e8%82%b2%e4%b8%8e%e5%81%a5%e5%ba%b7')
    pass