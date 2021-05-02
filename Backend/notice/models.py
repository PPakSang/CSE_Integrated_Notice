from django.db import models
from django.db.models.base import Model


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name

        
class Uni_post(models.Model):
    post_title = models.CharField(max_length=100, help_text='공지사항 이름')
    post_content = models.TextField(help_text='공지사항 내용')
    post_url = models.URLField(max_length=200)
    attachment_url = models.URLField(max_length=200)
    tag = models.ManyToManyField(Tag)

    "https://computer.knu.ac.kr/06_sub/02_sub.html?no=3294"
    "computer_3294"


    def __str__(self) -> str:
        return self.post_title