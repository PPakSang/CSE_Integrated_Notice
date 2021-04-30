# Generated by Django 3.2 on 2021-04-21 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_name', models.CharField(help_text='Enter your board_name', max_length=10)),
                ('post', models.TextField(help_text='Enter your post', max_length=1000)),
            ],
        ),
    ]