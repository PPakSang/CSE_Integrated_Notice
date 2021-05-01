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
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

