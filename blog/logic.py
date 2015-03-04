#-*- coding:utf-8 -*-
from functools import wraps
import datetime
from blog.models import *
from django.core.paginator import Paginator

ZEN_CONTENT = '''
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

ZEN_AUTHOR = '''The Zen of Python, by Tim Peters'''

PAGINATOR_SIZE = 10

class Zen(object):
    def __init__(self,content=None,author=None):
        self.content = content
        self.author = author

class InputException(Exception):
    def __init__(self, value):
        self.value = value
    def __unicode__(self):
        return self.value

def get_basic_output(objects=None, index=0, page_size=PAGINATOR_SIZE, request=None, clear_content=False):
    blog = Blog()
    if clear_content:
        request.session['search_content'] = ""
    if objects and index and page_size:
        pages = Paginator(objects, page_size)
        page = pages.page(index)
        return blog, pages, page
    else:
        return blog

def get_pre_or_next_article(pub_date):
    try:
        article_pre = Article.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    except Article.DoesNotExist as e:
        article_pre = [] 
    try:
        article_next = Article.objects.filter(pub_date__lt=pub_date).order_by('pub_date').last()
    except Article.DoesNotExist as e:
        article_next = []
    return article_pre, article_next

def page_view_analyze(func):
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        if request.META.has_key("REQUEST_URI"):
            url = request.META['REQUEST_URI']
        else:
            url = request.META['PATH_INFO'].encode("utf-8")
        ip = request.META['REMOTE_ADDR']
        today = datetime.date.today()
        #总访问量
        pvTotal = PageViewTotal.objects.get_or_create(url=url,ip=ip)[0]
        pvTotal.pv += 1
        pvTotal.save()
        #y今日访问量y
        pvToday = PageViewToday.objects.get_or_create(url=url,ip=ip, year=today.year,month=today.month,day=today.day)[0]
        pvToday.pv += 1
        pvToday.save()
        #本周访问量
        weekNow = int(today.strftime('%U'))
        pvWeek = PageViewWeek.objects.get_or_create(url=url,ip=ip,year=today.year,week=weekNow)[0]
        pvWeek.pv += 1
        pvWeek.save()
        #本月访问量
        pvMonth = PageViewMonth.objects.get_or_create(url=url,ip=ip, year=today.year,month=today.month)[0]
        pvMonth.pv += 1
        pvMonth.save()
        return func(request, *args, **kwargs)
    return returned_wrapper

class PageViewCount(object):
    def __init__(self, url='/', date=datetime.date.today()):
        try:
            pvToday = PageViewToday.objects.filter(url=url,year=date.year,month=date.month,day=date.day)
            self.today = SUMPV(pvToday)
        except PageViewToday.DoesNotExist as e:
            self.today = 0
        try:
            yesterday = date - datetime.timedelta(days=1)
            pvYesterday = PageViewToday.objects.filter(url=url,year=yesterday.year,month=yesterday.month,day=yesterday.day)
            self.yesterday = SUMPV(pvYesterday)
        except PageViewToday.DoesNotExist as e:
            self.yesterday = 0
        try:
            weekNow = int(date.strftime('%U'))
            pvWeek = PageViewWeek.objects.filter(url=url,year=date.year,week=weekNow)
            self.week = SUMPV(pvWeek)
        except PageViewWeek.DoesNotExist as e:
            self.week = 0
        try:
            pvMonth = PageViewMonth.objects.filter(url=url,year=date.year,month=date.month)
            self.month = SUMPV(pvMonth)
        except PageViewMonth.DoesNotExist as e:
            self.month = 0
        try:
            pvTotal = PageViewTotal.objects.filter(url=url)
            self.total = SUMPV(pvTotal)
        except PageViewTotal.DoesNotExist as e:
            self.total = 0

class Blog(object):
    def __init__(self):
        self.name = u"kevin's blog"
        self.keywards = u"小虫子,django,python"
        self.author = u"kevin"
        self.description = u"这是一个python程序员的博客"
        self.zen = Zen()
        self.showRequest = False
        self.zen.content = ZEN_CONTENT
        self.zen.author = ZEN_AUTHOR
        self.ranks = None
        self.comments = Comment.objects.all()
        if self.comments > 10:
            self.comments = self.comments[:10]
        self.pageView = PageViewCount()
        self.categories = [cat for cat in Category.objects.all() if cat.article_set.count() > 0]
        self.tags = Tag.objects.all()

