# pyright: reportMissingImports=false
from bs4 import BeautifulSoup as bs
from urllib import parse
import requests
import django
import random
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CIN.settings')
django.setup()
from notice.models import Uni_post,Tag

headers = {
    "Host": "computer.knu.ac.kr",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}


def get_data():
    def get_page_url(notice_type="2"):
        # 학사:2, 심컴:3, 글솝:4
        notice_type = f"_{notice_type}" if notice_type else ""
        return f"http://computer.knu.ac.kr/06_sub/02_sub{notice_type}.html"

    def isExisted(post):
        return False if random.randrange(0, 10) == 0 else True

    db = []

    while (True):
        req = requests.get(get_page_url(2), headers=headers)
        notice_list = bs(req.text, "html.parser").find("table", class_="table").find("tbody").find_all("tr")

        for p in notice_list:
            temp = p.find("a")

            post = Uni_post()
            post.post_title = temp.get("title")
            post.post_url = f"{get_page_url(2)}{temp.get('href')}"
            post.attachment_url = "123"
            
            
            
            

            # if not (isExisted(post)): # 원래는 db에 있는 id가지고 검증해야 함. 지금은 테스트를 위해 랜덤으로 둠
            #     contents = requests.get(post.post_url, headers=headers).text
            #     contents = bs(contents, "html.parser").find("div", class_="kboard-document-wrap left")
            #     post.contents = contents

            #     db.append(post)
            db.append(post)


        break # 원래는 딜레이 주고 무한반복 돌면서 새 글이 올라오는지 확인해야 함
    a = 0
    for item in db:
        # print(item.post_title, item.post_url)#, item.contents)
        if str(item.post_title).find('휴학') != -1:
            
            item.save()
            tag,flag = Tag.objects.get_or_create(name = '휴학') 
            item.tag.add(tag)

    # post_all = Uni_post.objects.all()
    # filtered_post = post_all.filter(post_title = '##')
    # for post in filtered_post :
        


            
            
    
        
        
    

    

if __name__ == '__main__':
     # Uni_post를 값으로 가지는 리스트
    get_data()
    
