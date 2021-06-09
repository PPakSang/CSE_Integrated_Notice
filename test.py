import requests
from bs4 import BeautifulSoup as bs
from requests.api import request

html = bs(requests.get('https://gp.knu.ac.kr/HOME/global/sub.htm?nav_code=glo1549935200').text,'html.parser')
# html.find_
url = "https://gp.knu.ac.kr"+ html.find("div",class_="paging").find_all("a")[0].get("href")

new = requests.get(url)
# bs().find_next_sibling
bs().find
html2 = bs(new.text,"html.parser").find("tbody").find_all("tr")[0].find_all("td")
# p

url = "https://gp.knu.ac.kr" + html2[1].find("a").get("href")

contents = bs(requests.get(url).text,'html.parser').find("div",class_="board_view")
# url = list("https://gp.knu.ac.kr"+url.find("a").get("href") for url in contents.find_all("li"))
print(contents.find_all("li"))
# print(contents.find_all("li")[0].find("a").text)
    
