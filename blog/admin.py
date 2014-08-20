from django.contrib import admin
from blog.models import *

class PageViewTodayAdmin(admin.ModelAdmin):
    list_display = ('url', 'pv', 'year','month', 'day')

class PageViewWeekAdmin(admin.ModelAdmin):
    list_display = ('url', 'pv', 'date')

class PageViewMonthAdmin(admin.ModelAdmin):
    list_display = ('url', 'pv', 'year','month')

class PageViewTotalAdmin(admin.ModelAdmin):
    list_display = ('url', 'pv', 'date')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )       

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )   

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date', 'pub_date', )   
    filter_horizontal=('tags',)
    search_fields=('title','content')
    list_filter=('tags',)
    ording=("pub_date",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'article',)

admin.site.register(PageViewToday, PageViewTodayAdmin)
admin.site.register(PageViewWeek, PageViewWeekAdmin)
admin.site.register(PageViewMonth, PageViewMonthAdmin)
admin.site.register(PageViewTotal, PageViewTotalAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
