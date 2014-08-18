from django.contrib import admin
from blog.models import PageView,Blog,Category,Tag,Article,Comment

class PageViewAdmin(admin.ModelAdmin):
    list_display = ('today', 'yesterday', 'week', 'month', 'total')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_view')

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

admin.site.register(PageView, PageViewAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
