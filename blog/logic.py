#-*- coding:utf-8 -*-
from functools import wraps
import datetime
from blog.models import *

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

def page_view_analyze(func):
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        url = request.META['REQUEST_URI']
        today = datetime.date.today()
        #总访问量
        pvTotal = PageViewTotal.objects.get_or_create(url=url)[0]
        pvTotal.pv += 1
        pvTotal.save()
        #y今日访问量y
        pvToday = PageViewToday.objects.get_or_create(url=url,year=today.year,month=today.month,day=today.day)[0]
        pvToday.pv += 1
        pvToday.save()
        #本周访问量
        weekNow = int(today.strftime('%U'))
        pvWeek = PageViewWeek.objects.get_or_create(url=url,year=today.year,week=weekNow)[0]
        pvWeek.pv += 1
        pvWeek.save()
        #本月访问量
        pvMonth = PageViewMonth.objects.get_or_create(url=url,year=today.year,month=today.month)[0]
        pvMonth.pv += 1
        pvMonth.save()
        return func(request, *args, **kwargs)
    return returned_wrapper

class PageViewLogic(object):
    def __init__(self, url='/', date=datetime.date.today()):
        try:
            pvToday = PageViewToday.objects.get(url=url,year=date.year,month=date.month,day=date.day)
            self.today = pvToday.pv
        except PageViewToday.DoesNotExist, e:
            self.today = 0
        try:
            yesterday = date - datetime.timedelta(days=1)
            pvYesterday = PageViewToday.objects.get(url=url,year=yesterday.year,month=yesterday.month,day=yesterday.day)
            self.yesterday = pvYesterday.pv
        except PageViewToday.DoesNotExist, e:
            self.yesterday = 0
        try:
            weekNow = int(date.strftime('%U'))
            pvWeek = PageViewWeek.objects.get(url=url,year=date.year,week=weekNow)
            self.week = pvWeek.pv
        except PageViewWeek.DoesNotExist, e:
            self.week = 0
        try:
            pvMonth = PageViewMonth.objects.get(url=url,year=date.year,month=date.month)
            self.month = pvMonth.pv
        except PageViewMonth.DoesNotExist, e:
            self.month = 0
        try:
            pvTotal = PageViewTotal.objects.get(url=url)
            self.total = pvTotal.pv
        except PageViewTotal.DoesNotExist, e:
            self.total = 0

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
        self.comments = Comment.objects.all()
        if self.comments > 10:
            self.comments = self.comments[:10]
        self.pageView = PageViewLogic()
        self.categories = Category.objects.all()
        self.tags = Tag.objects.all()

