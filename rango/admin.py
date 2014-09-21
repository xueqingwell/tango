from django.contrib import admin
from rango.models import Category, Page,UserProfile


class PageyAdmin(admin.ModelAdmin):
    list_display = ['title','category','url']


admin.site.register(Category)
admin.site.register(Page,PageyAdmin)
admin.site.register(UserProfile)