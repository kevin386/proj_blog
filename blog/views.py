#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response,get_list_or_404
from django.http import Http404
from blog.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

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
            pass

def submit_comment(request,id):
    blog = Blog()
    errors = []
    content = request.POST.get('comment_content')
    user_name = request.POST.get('user_name')
    email = request.POST.get('email')
    if not user_name:
        errors.append("Please input user name!")
    if not content:
        errors.append("Please input content!")
    if user_name and content:
        article = get_object_or_404(Article,id=id)
        com = Comment(user_name=user_name,email=email,content=content,article=article)
        com.save()
        try:
            preArticle = Article.objects.filter(pub_date__gt=article.pub_date).order_by('pub_date').first()
        except Article.DoesNotExist, e:
            preArticle = [] 
        try:
            nextArticle = Article.objects.filter(pub_date__lt=article.pub_date).order_by('pub_date').last()
        except Article.DoesNotExist, e:
            nextArticle = [] 
    return HttpResponseRedirect(reverse("article_by_id", kwargs={"id":id}))

def search_articel(request):
    blog = Blog()
    content = request.POST.get('search_content')
    articles = Article.objects.filter(title__icontains=content)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def about_me(request):
    blog = Blog()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def vote(request,id):
    vote_count = 0
    if not request.session.get('has_voted_'+str(id), False):
        article = get_object_or_404(Article,id=id)
        article.vote_count += 1;
        article.save()
        vote_count = article.vote_count
        request.session['has_voted_'+str(id)] = True
    return HttpResponse(vote_count)

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
    return render_to_response('article.html', locals(), context_instance=RequestContext(request))

def category(request,id):
    blog = Blog()
    cat = get_object_or_404(Category,id=id)
    try:
        articles = cat.article_set.all().order_by('-pub_date')
    except Exception, e:
        pass
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def home(request):
    blog = Blog()
    try:
        articles = Article.objects.all().order_by('-pub_date')
    except Exception, e:
        pass
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
