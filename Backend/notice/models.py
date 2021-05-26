from django.db import models
from django.db.models.base import Model


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name

        
class Uni_post(models.Model):
    post_origin = models.CharField(max_length=50, help_text='공지사항 구분')
    post_title = models.CharField(max_length=100, help_text='공지사항 이름')
    post_contents = models.TextField(help_text='공지사항 내용')
    post_author = models.CharField(max_length=20, help_text="공지사항 작성자")
    post_date = models.CharField(max_length=50, help_text="공지사항 등록일")
    post_url = models.URLField(max_length=200)
    attachment_info = models.CharField(max_length=100, help_text='첨부파일 정보', null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.post_title
