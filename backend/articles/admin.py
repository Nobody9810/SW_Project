from django.contrib import admin
from .models import *

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'total_views', 'likes', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'created_at'

@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'is_published', 'total_views', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BookReviewCategory)
class BookReviewCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'total_views', 'updated_at']
    list_filter = ['is_published', 'category', 'created_at']
    search_fields = ['title', 'content', 'author']

# 注册其他模型...
admin.site.register(Opinion)
admin.site.register(Literature)
admin.site.register(QA)
admin.site.register(Translation)
admin.site.register(History)
admin.site.register(Paper)
admin.site.register(ClassicBook)
admin.site.register(Library)
admin.site.register(Scripture)
admin.site.register(ScriptureChapter)
admin.site.register(Contact)