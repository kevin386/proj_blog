#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response,get_list_or_404
from django.http import Http404
from blog.models import *
from django.http import HttpResponse

zen_content = '''
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

zen_author = '''The Zen of Python, by Tim Peters'''

class Zen(object):
    def __init__(self,content=None,author=None):
        self.content = content
        self.author = author

class Blog(object):
    def __init__(self):
        self.name = "kevin's blog"
        self.keywards = u"小虫子,django,python"
        self.author = "kevin"
        self.description = u"这是一个python程序员的博客"
        self.zen = Zen()
        self.showRequest = False
        self.zen.content = zen_content
        self.zen.author = zen_author
        self.ranks = None
        self.lastestComments = None
        #self.pageView = PageView.objects.get(id=1)
        try:
            self.categories = [cat for cat in Category.objects.all()]
        except Category.DoesNotExist, e:
            raise Http404

def aboutme(request):
    pass

def vote(request,id):
    article = get_object_or_404(Article,id=id)
    article.vote_count += 1;
    article.save()
    return HttpResponse(article.vote_count)

def article(request,id):
    blog = Blog()
    article = get_object_or_404(Article,id=id)
    try:
		preArticle = Article.objects.filter(pub_date__gt=article.pub_date).order_by('pub_date').first()
    except Article.DoesNotExist, e:
        preArticle = [] 
    try:
        nextArticle = Article.objects.filter(pub_date__lt=article.pub_date).order_by('pub_date').last()
    except Article.DoesNotExist, e:
        nextArticle = [] 
    return render_to_response('article.html', locals())

def category(request,id):
    blog = Blog()
    cat = get_object_or_404(Category,id=id)
    try:
        articles = cat.article_set.all().order_by('-pub_date')
    except Exception, e:
        pass
    return render_to_response('index.html', locals())

def home(request):
    blog = Blog()
    try:
        articles = Article.objects.all().order_by('-pub_date')
    except Exception, e:
        pass
    return render_to_response('index.html', locals())
