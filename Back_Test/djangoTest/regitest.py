#일반 파이썬 파일을 django 파일로 변경 후 데이터를 등록하는 파일


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notice.settings')
#Djano setting module 을 따를건데 이건 notice.settings 에 있다
import django
django.setup()
from board.models import Board

def data_set():
    data=[]

    for i in range(10):
        data.append(Board(board_name=i,post=i))

    return data
if __name__ == '__main__': #파이썬 파일을 직접 실행시킬때만 작동
    data=data_set() #list

    Board.objects.bulk_create(data)
    

    
