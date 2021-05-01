from django.contrib import admin
from .models import Uni_post,Tag
# Register your models here.


admin.site.register(Uni_post)
admin.site.register(Tag)

# @admin.register(Uni_post)
# class Uni_post_Admin(admin.ModelAdmin):
#     pass

# @admin.register(Tag)
# class Tag_Admin(admin.ModelAdmin):
#     pass