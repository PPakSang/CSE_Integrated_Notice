# pyright: reportMissingImports=false
from bs4 import BeautifulSoup as bs
from urllib import parse
import requests
import django
import random
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CIN.settings')
django.setup()
from notice.models import Uni_post, Tag

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
            post.attachment_url = ""
            post.tags__name = ""

            if not (isExisted(post)): # 원래는 db에 있는 id가지고 검증해야 함. 지금은 테스트를 위해 랜덤으로 둠
                contents = requests.get(post.post_url, headers=headers).text
                contents = bs(contents, "html.parser").find("div", class_="kboard-document-wrap left")
                post.contents = contents

                db.append(post)


        break # 원래는 딜레이 주고 무한반복 돌면서 새 글이 올라오는지 확인해야 함

    for item in db:
        print(item.post_title, item.post_url)#, item.contents)

    

if __name__ == '__main__':
    # data = get_data() # Uni_post를 값으로 가지는 리스트
    # Uni_post.objects.bulk_create(data)
    rn= random.randrange(0, 100)
    post = Uni_post(post_title=f"타이틀{rn}", post_content="컨텐츠", post_url="http://d.net", attachment_url="http://a.com")
    post.save()
    post.tags.add(Tag.objects.get(name="대학원"), Tag.objects.get(name="멘토링"))
    print(post)
    # M2M 필드는 db에 write 된 이후에 값을 설정할 수 있음 -> 미리 설정된 객체 리스트를 만들어 놓고 한 번에 추가할 수 없음.
    # 따라서, get_data()에서는 tags 필드를 제외한 값만 준비해 두고, bulk_create()이후에 태그를 추가해야 할 듯
    # print(Uni_post.objects.all()[0].post_url)
