# Generated by Django 3.2.2 on 2021-05-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0004_auto_20210518_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='uni_post',
            name='attachment_title',
            field=models.CharField(default=str, help_text='첨부파일 이름', max_length=100),
            preserve_default=False,
        ),
    ]