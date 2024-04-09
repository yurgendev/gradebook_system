from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'likes_count')
    search_fields = ['title', 'content']
    readonly_fields = ('likes_count',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'image', 'video', 'author')
        }),
        ('Likes', {
            'fields': ('likes_count',)
        }),
    )