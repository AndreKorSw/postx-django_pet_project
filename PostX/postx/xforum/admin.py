from django.contrib import admin
from .models import *
# Register your models here.




class XforumAdmin(admin.ModelAdmin):
     list_display = ("title", "id", "time_create", "photo", "is_published",)
     list_display_links = ('id', "title",)
     search_fields = ("title", "content",)
     list_editable = ('is_published',)
     prepopulated_fields = {"slug":("title",)}
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_display_links = ("id", "name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Xforum, XforumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments)
admin.site.register(Profile)