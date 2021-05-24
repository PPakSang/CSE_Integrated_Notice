"""
DEPRECATED SINCE 2021-05-21
Use manage.py -runserver instead
"""


"""
# pyright: reportMissingImports=false
from bs4 import BeautifulSoup as bs
import requests
import django
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


def getData():
    def get_page_url(notice_type="2"):
        # 학사:2, 심컴:3, 글솝:4
        notice_type = f"_{notice_type}" if notice_type else ""
        return f"http://computer.knu.ac.kr/06_sub/02_sub{notice_type}.html"

    def isExisted(post):
        try:
            post.__class__.objects.get(post_url=post.post_url)
        except Exception as e:
            return False
        else:
            print("이미 DB에 존재하는 공지사항입니다.", post.post_title)
            return True

    def setPostTag(post, *tagnames):
        tags = list(map(lambda t: Tag.objects.get(name=t), tagnames))
        post.tags.add(*tags)


    while (True):
        req = requests.get(get_page_url(2), headers=headers)
        notice_list = bs(req.text, "html.parser").find("table", class_="table").find("tbody").find_all("tr")

        for p in notice_list:
            # 상단 고정된 공지사항일 경우 크롤링하지 않음
            if (p.find(class_="bbs_num").text == "공지"):
                continue
            
            # 게시물 인스턴스 생성 후 값 저장
            post = Uni_post()
            post.post_url = f"{get_page_url(2)}{p.find('a').get('href')}"
            post.post_title = p.find('a').get("title")
            post.post_author = p.find("td", class_="bbs_writer").text
            post.post_date = p.find("td", class_="bbs_date").text

            # DB에 존재하지 않는 게시글일 경우 게시글 내용 크롤링하여 저장
            if not (isExisted(post)):
                # 게시글 내용 확인하기 위해 GET 요청
                data = requests.get(post.post_url, headers=headers).text
                # 게시글 내용 파싱 후 저장
                contents = bs(data, "html.parser").find("div", class_="kboard-document-wrap left")
                post.post_contents = contents.prettify()
                # 첨부파일 정보 파싱 후 저장
                attach = bs(data, "html.parser").find_all("div", class_="kboard-attach")
                attach_url = map(lambda tag: tag.find("a").get("href"), attach)
                attach_name = map(lambda tag: tag.find("a").text, attach)
                post.attachment_url = ", ".join(attach_url)
                post.attachment_title = ", ".join(attach_name)
                # 인스턴스 DB에 기록
                post.save()
                # M2M 필드(게시물 태그) 설정
                setPostTag(post, "멘토링", "대학원")
                # print(post.post_contents, post.attachment_url)

        break # 원래는 딜레이 주고 무한반복 돌면서 새 글이 올라오는지 확인해야 함

    
        
        
    


if __name__ == '__main__':
    for post in Uni_post.objects.all():
        post.delete()
    getData()
    # data = get_data() # Uni_post를 값으로 가지는 리스트
    # Uni_post.objects.bulk_create(data)
    # rn = random.randrange(0, 100)
    # post = Uni_post(post_title=f"타이틀{rn}", post_content="컨텐츠", post_url="http://d.net", attachment_url="http://a.com")
    # post.save()
    # post.tags.add(Tag.objects.get(name="대학원"), Tag.objects.get(name="멘토링"))
    # print(post)
    # M2M 필드는 db에 write 된 이후에 값을 설정할 수 있음 -> 미리 설정된 객체 리스트를 만들어 놓고 한 번에 추가할 수 없음.
    # 따라서, get_data()에서는 tags 필드를 제외한 값만 준비해 두고, bulk_create()이후에 태그를 추가해야 할 듯
    # print(Uni_post.objects.all()[0].post_url)
"""
