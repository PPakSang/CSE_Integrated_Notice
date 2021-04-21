from django.contrib import admin
from catalog.models import Author,Book,BookInstance,Genre,Language
# Register your models here.


admin.site.register(Book)
admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)



@admin.register(Author)
class registerAdmin(admin.ModelAdmin):
    list_display=('last_name','first_name','date_of_birth','date_of_death')

