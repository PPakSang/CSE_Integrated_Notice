from django.contrib import admin
from catalog.models import Author,Book,BookInstance,Genre,Language
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)


@admin.register(Author)
class registerAdmin(admin.ModelAdmin):
    list_display=('last_name','first_name','date_of_birth','date_of_death')

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter=('status','due_back')
    list_display=('id','status','due_back')


user=User.objects.create_user('sh3','','1234')

user.first_name='홍1'
user.last_name='길동테스트'
user.save()