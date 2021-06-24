#!/usr/bin/env python
# pyright: reportMissingImports=false
from bs4 import BeautifulSoup as bs
from urllib import parse
import threading
import requests
import django
import json
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

    def get_page_url(notice_type=2, page=0):
        # 학사:2, 심컴:3, 글솝:4
        notice_type = f"_{notice_type}" if notice_type else ""
        pageinfo = f"?page={page}" if page else ""
        return f"http://computer.knu.ac.kr/06_sub/02_sub{notice_type}.html{pageinfo}"

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
        tags = list(map(lambda t: Tag.objects.get_or_create(name=t, origin=post.post_origin)[0], tagnames))
        post.tags.add(*tags)

    def getPostTag(title: str, contents: str) -> list:
        tag_data = {
            "CUBE/채용" : ("CUBE","cube","채용","인턴"),
            "근로/튜터": ("근로", "튜터", "TUTOR", "tutor", "Tutor"),
            "대회": ("대회","콘테스트","공모전","특허청","아이디어","모각코"),
            "마일리지": ("마일리지", ),
            "세미나": ("세미나", ),
            "인재개발원" : ("인재개발원","인재"),
            "장학금": ("장학금", "장학생", "장학재단","학자금"),
            "졸업": ("졸업", ),
            "창업" : ("창업"),
            "휴/복학": ("휴학", "복학"),
            "SW 중심대학": ("[SW중심대학]", ),
        }
        tag_result = []

        for tag in tag_data.keys():
            for keyword in tag_data[tag]:
                if (keyword in title or keyword in contents):
                    tag_result.append(tag)
                    break

        return tag_result if tag_result else ["기타"]

    current_page = 1
    req = requests.get(get_page_url(origin, current_page), headers=headers)
    soup = bs(req.text, "html.parser")

    # DB에 저장된 게시물의 총 개수가 50개 미만이면 최대 5페이지를 한번에 크롤링
    if (Uni_post.objects.filter(post_origin = "컴퓨터학부").count() < 50):
        try:
            lastpage = int(parse.parse_qs(soup.find_all("a", class_="paging-arrow")[-1]["href"][1:])["page"][0])
        except IndexError:
            lastpage = 1
        finally:
            lastpage = min(lastpage, 5)
    else:
        lastpage = 1

    while (True):
        req = requests.get(get_page_url(origin, current_page), headers=headers)
        notice_list = bs(req.text, "html.parser").find("table", class_="table").find("tbody").find_all("tr")

        for p in notice_list:
            # 상단 고정된 공지사항일 경우 크롤링하지 않음
            if (p.find(class_="bbs_num").text == "공지"):
                continue

            # 게시물 인스턴스 생성 후 값 저장
            post = Uni_post()
            post.post_url = f"{get_page_url(origin)}{p.find('a').get('href')}"
            post.post_title = p.find('a').get("title")

            # DB에 존재하지 않는 게시글일 경우 게시글 내용 크롤링하여 저장
            if not (isExisted(post)):
                post.post_author = p.find("td", class_="bbs_writer").text
                post.post_date = p.find("td", class_="bbs_date").text
                post.post_origin = "컴퓨터학부"

                # 게시글 내용 확인하기 위해 GET 요청
                data = requests.get(post.post_url, headers=headers).text
                # 게시글 내용 파싱
                contents = bs(data, "html.parser").find("div", class_="kboard-document-wrap left")

                # 상대 경로로 등록된 이미지 주소들을 절대 경로로 변경
                for img in contents.find_all("img", src=True):
                    if (img["src"].startswith("/")):
                        img["src"] = f"http://computer.knu.ac.kr{img['src']}"

                # 상대 경로로 등록된 첨부파일 주소들을 절대 경로로 변경
                for a in contents.find_all("a", href=True):
                    if (a["href"].startswith("/")):
                        a["href"] = f"http://computer.knu.ac.kr{a['href']}"

                # 첨부파일 정보 파싱 후 저장
                attach = contents.find_all("div", class_="kboard-attach")
                attach_url = map(lambda tag: tag.find("a").get("href"), attach)
                attach_name = map(lambda tag: tag.find("a").text, attach)
                attach_info = {title: url for title, url in zip(attach_name, attach_url)}
                post.attachment_info = json.dumps(attach_info, ensure_ascii=False)
                
                # 게시글 내용에서 필요없는 부분 삭제
                for cls in ("kboard-title", "kboard-detail", "kboard-attach", "kboard-control"):
                    part = contents.find_all("div", class_=cls)
                    for p in part:
                        if (p is not None):
                            p.decompose()

                # 게시글 내용 저장
                post.post_contents = contents.prettify()

                # 인스턴스 DB에 기록
                post.save()
                # M2M 필드(게시물 태그) 설정
                setPostTag(post, f"컴학_{typeEnum[origin]}", *getPostTag(post.post_title, contents.get_text()))

        print(f"---------------{threading.current_thread().name}, {typeEnum[origin]}, {current_page}/{lastpage}---------------")
        if (current_page < lastpage):
            current_page += 1
        else:
            lastpage = 1
            current_page = 1
            time.sleep(60)


def getData2():
    def get_page_url(page):
        pageinfo = f"btin.page={page}" if page else ""
        return f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?{pageinfo}&menu_idx=42"

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
        tags = list(map(lambda t: Tag.objects.get_or_create(name=t, origin=post.post_origin)[0], tagnames))
        post.tags.add(*tags)

    def getPostTag(title: str, contents: str) -> list:
        tag_data = {
            "연계/융합/복수전공": ("연계전공", "융합전공", "복수전공"),
            "대학원": ("석사", "대학원"),
            "수강신청": ("수강신청", "수강변경", "수강정정", "꾸러미"),
            "등록금": ("수강료", "등록금"),
            "졸업": ("졸업", ),
            "휴/복학": ("휴학", "복학"),
            "계절학기": ("계절학기", "계절수업", "여름계절", "겨울계절")
        }
        tag_result = []

        for tag in tag_data.keys():
            for keyword in tag_data[tag]:
                if (keyword in title or keyword in contents):
                    tag_result.append(tag)
                    break

        return tag_result if tag_result else ["기타"]

    current_page = 1
    # DB에 저장된 게시물의 총 개수가 50개 미만이면 최대 5페이지를 한번에 크롤링
    if (Uni_post.objects.filter(post_origin = "경북대학교 학사공지").count() < 50):
        lastpage = 5
    else:
        lastpage = 1
    while (True):
        req = requests.get(get_page_url(current_page), headers=headers)
        notice_list = bs(req.text, "html.parser").find("div", class_="board_list").find("tbody").find_all("tr")

        for p in notice_list:
            # 상단 고정된 공지사항일 경우 크롤링하지 않음
            if (p.find(class_="num").text == "공지"):
                continue

            # 게시물 인스턴스 생성 후 값 저장
            post = Uni_post()
            post_no = p.find('a').get('href')
            post_no = int(post_no[19:post_no.index("',")])
            post.post_url = f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdViewBtin.action?btin.doc_no={post_no}&btin.appl_no=000000&btin.page=1&btin.search_type=&btin.search_text=&popupDeco=&btin.note_div=row&menu_idx=42"
            post.post_title = p.find('a').text.lstrip().rstrip()

            # DB에 존재하지 않는 게시글일 경우 게시글 내용 크롤링하여 저장
            if not (isExisted(post)):
                post.post_author = p.find("td", class_="writer").text
                post.post_date = p.find("td", class_="date").text
                post.post_origin = "경북대학교 학사공지"

                # 게시글 내용 확인하기 위해 GET 요청
                data = requests.get(post.post_url, headers=headers).text
                # 게시글 내용 파싱
                soup = bs(data, "html.parser")
                contents = soup.find("div", class_="board_cont")

                # 첨부파일 정보 파싱 후 저장
                try:
                    attach = soup.find("div", class_="attach").find_all("li")
                except AttributeError:
                    post.attachment_info = {}
                else:
                    attach_url = map(lambda file_no: f"https://my.knu.ac.kr/stpo/stpo/bbs/btin/downloadServlet.action?appFile.bbs_cde=812&appFile.doc_no={post_no}&appFile.appl_no=000000&appFile.file_nbr={file_no}&bbs_cde=812&btin.doc_no={post_no}&btin.bbs_cde=812&btin.appl_no=000000", range(len(attach)))
                    attach_name = map(lambda tag: tag.find("a").text, attach)
                    attach_info = {title: url for title, url in zip(attach_name, attach_url)}
                    post.attachment_info = json.dumps(attach_info, ensure_ascii=False)

                # 게시글 내용 저장
                post.post_contents = contents.prettify()

                # 인스턴스 DB에 기록
                post.save()
                # M2M 필드(게시물 태그) 설정
                setPostTag(post, *getPostTag(post.post_title, contents.get_text()))

        print(f"---------------{threading.current_thread().name}, {'KNU'}, {current_page}/{lastpage}---------------")
        if (current_page < lastpage):
            current_page += 1
        else:
            lastpage = 1
            current_page = 1
            time.sleep(60)

#국제 교류처
def getData3():
    def get_page_url(page):
        # 첫번째 페이지에서 나머지 페이지 파싱하는 방식

        #첫번째 페이지
        base_url = "https://gp.knu.ac.kr/HOME/global/sub.htm?nav_code=glo1549935200"

        if page > 10 :
            page = 1

        if page == 1 :
            return base_url
        else :
            req = requests.get(base_url)
            parsed_html = bs(req.text,"html.parser")
            pages = parsed_html.find("div",class_="paging").find_all("a")
            # 구조상 첫번째 a태그가 2부터 시작이다
            href = pages[page-1]
        req = requests.get(base_url)
        parsed_html = bs(req.text,"html.parser")
        pages = parsed_html.find("div",class_="paging").find_all("a")
        # 구조상 두번째 a태그가 0번째 array부터 시작이다
        href = pages[page-2].get("href")

        return "https://gp.knu.ac.kr"+href

    def isExisted(post):
        try:
            post.__class__. objects.get(post_url=post.post_url)
        except Exception as e:
            print("DB에 추가합니다.", post.post_title)
            return False
        else:
            # print("이미 DB에 존재하는 공지사항입니다.", post.post_title)
            return True

    def setPostTag(post, *tagnames):
        tags = list(map(lambda t: Tag.objects.get_or_create(name=t, origin=post.post_origin)[0], tagnames))
        post.tags.add(*tags)

    def getPostTag(title: str, contents: str) -> list:
        tag_data = {
            "공모전": ("공모전", ),
            "대외활동": ("대외활동", ),
            "교내 프로그램": ("교내", "교내 프로그램", "교내프로그램"),
            "유학": ("유학","복수학위","교환학생","아시아","유럽","미국"),
            "강연/세미나": ("강연", "세미나"),
            "취업/인턴": ("취업","인턴"),
            "장학": ("장학"),
        }
        tag_result = []

        for tag in tag_data.keys():
            for keyword in tag_data[tag]:
                if (keyword in title or keyword in contents):
                    tag_result.append(tag)
                    break

        return tag_result if tag_result else ["기타"]

    current_page = 1
    # DB에 저장된 게시물의 총 개수가 50개 미만이면 최대 5페이지를 한번에 크롤링
    if (Uni_post.objects.filter(post_origin = "국제교류처").count() < 50):
        lastpage = 5
    else:
        lastpage = 1

    while (True):
        req = requests.get(get_page_url(current_page))
        notice_list = bs(req.text, "html.parser").find("tbody").find_all("tr")
        for p in notice_list:
            # p[n] 0 == 공지 or 글 번호, 1 == 제목, 2 == 첨부파일, 3 == author, 4 == date, 5 == 조회수
            p = p.find_all("td")

            # 상단 고정된 공지사항일 경우 크롤링하지 않음
            if (p[0].text == "공지"):
                continue
            
            # 게시물 인스턴스 생성 후 값 저장
            post = Uni_post()

            #urlencode
            #먼저 url을 parsing 한다 (path 기준으로 앞 뒤)
            url = parse.urlparse("https://gp.knu.ac.kr" + (p[1].find("a").get("href")))
            query = parse.parse_qs(url.query)
            qs = parse.urlencode(query,doseq=True)
            post.post_url =  f"https://gp.knu.ac.kr{url.path}?{qs}"
            post.post_title = p[1].text.strip()
            # DB에 존재하지 않는 게시글일 경우 게시글 내용 크롤링하여 저장
            if not (isExisted(post)):
                post.post_author = p[3].text
                post.post_date = p[4].text
                post.post_origin = "국제교류처"

                # 게시글 내용 확인하기 위해 GET 요청
                data = requests.get(post.post_url).text
                # 게시글 내용 파싱
                soup = bs(data, "html.parser")
                contents = soup.find("div", class_="board_view")
                # 첨부파일 정보 파싱 후 저장
                try:
                    attach = contents.find_all("li")
                except AttributeError:
                    post.attachment_info = {}
                else:
                    try:
                        attach_url = list(("https://gp.knu.ac.kr" + url.find("a").get("href")[5:]) for url in attach)
                        attach_name = map(lambda tag: tag.find("a").text, attach)
                        attach_info = {title: url for title, url in zip(attach_name, attach_url)}
                        post.attachment_info = json.dumps(attach_info, ensure_ascii=False)
                    except: # 글중에 li 있으면 그냥 pass
                        pass

                contents.find("table").decompose()
                # 게시글 내용 저장
                post.post_contents = contents.prettify()

                # 인스턴스 DB에 기록
                post.save()
                # M2M 필드(게시물 태그) 설정
                setPostTag(post, *getPostTag(post.post_title, contents.get_text()))

        print(f"---------------{threading.current_thread().name}, {'국제교류처'}, {current_page}/{lastpage}---------------")
        if (current_page < lastpage):
            current_page += 1
        else:
            lastpage = 1
            current_page = 1
            time.sleep(60)



def main():
    # auto-reloader 프로세스가 아닌 Django 메인 프로세스일때만 크롤러 스레드 실행
    if (os.environ.get("RUN_MAIN")):
        th = [threading.Thread(target=getData, name=f"th_crawler_{i}", args=(i, ), daemon=True) for i in (0, 2, 3, 4)]
        for t in th:
            t.start()
            print(f"{t.name} 스레드 시작됨")
        th = [threading.Thread(target=getData2, name=f"th_crawler_knu", daemon=True) for i in (1, )]
        for t in th:
            t.start()
            print(f"{t.name} 스레드 시작됨")
        th = [threading.Thread(target=getData3, name=f"th_crawler_국제교류처", daemon=True) for i in (1, )]
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
    if (sys.argv[1] == "dropall"):
        post = Uni_post.objects.all()
        post.delete()

        print("저장된 모든 게시물을 삭제했습니다.")
        sys.exit(0)
    main()
