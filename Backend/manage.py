#!/usr/bin/env python
# pyright: reportMissingImports=false
"""Django's command-line utility for administrative tasks."""
from bs4 import BeautifulSoup as bs
import threading
import requests
import django
import time
import sys
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

def getData(origin):
    # return
    typeEnum = ("전체", "", "학사", "심컴", "글솝")

    def get_page_url(notice_type=2):
        # 학사:2, 심컴:3, 글솝:4
        notice_type = f"_{notice_type}" if notice_type else ""
        return f"http://computer.knu.ac.kr/06_sub/02_sub{notice_type}.html"

    def isExisted(post):
        try:
            post.__class__.objects.get(post_url=post.post_url)
        except Exception as e:
            print("DB에 추가합니다.", post.post_title)
            return False
        else:
            # print("이미 DB에 존재하는 공지사항입니다.", post.post_title)
            return True

    def setPostTag(post, *tagnames):
        tags = list(map(lambda t: Tag.objects.get(name=t), tagnames))
        post.tags.add(*tags)

    while (True):
        req = requests.get(get_page_url(origin), headers=headers)
        notice_list = bs(req.text, "html.parser").find("table", class_="table").find("tbody").find_all("tr")

        for p in notice_list:
            # 상단 고정된 공지사항일 경우 크롤링하지 않음
            if (p.find(class_="bbs_num").text == "공지"):
                continue

            # 게시물 인스턴스 생성 후 값 저장
            post = Uni_post()
            post.post_url = f"{get_page_url(origin)}{p.find('a').get('href')}"
            post.post_title = p.find('a').get("title")
            post.post_author = p.find("td", class_="bbs_writer").text
            post.post_date = p.find("td", class_="bbs_date").text
            post.post_origin = f"컴퓨터학부_{typeEnum[origin]}"

            # DB에 존재하지 않는 게시글일 경우 게시글 내용 크롤링하여 저장
            if not (isExisted(post)):
                # 게시글 내용 확인하기 위해 GET 요청
                data = requests.get(post.post_url, headers=headers).text
                # 게시글 내용 파싱
                contents = bs(data, "html.parser").find("div", class_="kboard-document-wrap left")

                # 상대 경로로 등록된 이미지 주소들을 절대 경로로 변경
                for img in contents.findAll("img", src=True):
                    if (img["src"].startswith("/")):
                        img["src"] = f"http://computer.knu.ac.kr{img['src']}"

                # 상대 경로로 등록된 첨부파일 주소들을 절대 경로로 변경
                for a in contents.findAll("a", href=True):
                    if (a["href"].startswith("/")):
                        a["href"] = f"http://computer.knu.ac.kr{a['href']}"

                # 첨부파일 정보 파싱 후 저장
                attach = contents.find_all("div", class_="kboard-attach")
                attach_url = map(lambda tag: tag.find("a").get("href"), attach)
                attach_name = map(lambda tag: tag.find("a").text, attach)
                post.attachment_url = ", ".join(attach_url)
                post.attachment_title = ", ".join(attach_name)

                # 게시글 내용에서 필요없는 부분 삭제
                for cls in ("kboard-detail", "kboard-attach", "kboard-control"):
                    part = contents.find("div", class_=cls)
                    if (part is not None):
                        part.decompose()

                # 게시글 내용 저장
                post.post_contents = contents.prettify()

                # 인스턴스 DB에 기록
                post.save()
                # M2M 필드(게시물 태그) 설정
                setPostTag(post, f"컴학_{typeEnum[origin]}", "멘토링")

        print(f"---------------{threading.current_thread().name}, {typeEnum[origin]}---------------")
        time.sleep(10)
        # break  # 원래는 딜레이 주고 무한반복 돌면서 새 글이 올라오는지 확인해야 함


def main():
    # auto-reloader 프로세스가 아닌 Django 메인 프로세스일때만 크롤러 스레드 실행
    if (os.environ.get("RUN_MAIN")):
        th = [threading.Thread(target=getData, name=f"th_crawler_{i}", args=(i, ), daemon=True) for i in (0, 2, 3, 4)]
        for t in th:
            t.start()
            print(f"{t.name} 스레드 시작됨")

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CIN.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    for post in Uni_post.objects.all():
        # post.delete()
        pass
    main()
