from django.db import models

# Create your models here.


class Board(models.Model):
    board_name=models.CharField(max_length=100,help_text='Enter your board_name')
    post=models.TextField(max_length=1000,help_text='Enter your post')
    
    class Meta:
        pass# ordering=['-board_name']  # DB에 저장되는 순서

    def __str__(self):
        return self.board_name
