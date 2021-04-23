import requests
from bs4 import BeautifulSoup
arr=[]

for i in range(1,5): #i = 공지사항 페이지 우선 5번째 페이지 까지만
    url=requests.get('https://computer.knu.ac.kr/06_sub/02_sub.html?page='+str(i)+'&key=&keyfield=&category=&bbs_code=Site_BBS_25')

    parsed=BeautifulSoup(url.content,'html.parser')

    a_title=parsed.findAll('a',attrs={'title':True,'target':False})  #a태그 중 타이틀이 있는것과 target이 없는것


    for title in a_title: #조건에 맞는 태그 중 title만을 뽑을 때
        arr.append(title['title'])


for data in arr:  # 공지사항 키워드 입력 시 그 데이터만 제공 ==data
    if data.find('장학') == True:
        print(data)


