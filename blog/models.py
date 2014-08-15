#-*- coding:utf-8 -*-
from django.db import models
import datetime
from utils import utils
from django.utils import timezone

class PageView(models.Model):
    today = models.IntegerField("今日访问量",default=0)
    yesterday = models.IntegerField("昨天访问量",default=0)
    week = models.IntegerField("本周访问量",default=0)
    month = models.IntegerField("本月访问量",default=0)
    total = models.IntegerField("总访问量",default=0)
    def __unicode__(self):
        return u"访问量统计"

class Blog(models.Model):
    title = models.CharField("博客名称", max_length=128)
    page_view = models.ForeignKey(PageView, verbose_name="页面访问统计")
    def __unicode__(self):
        return self.title
        
class Category(models.Model):
    name = models.CharField("分类", max_length=64)
    def __unicode__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField("标签", max_length=64)
    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField("标题", max_length=128)
    #一个分类有多篇文章（多对一关系）
    category = models.ForeignKey(Category,verbose_name="分类")
    #一篇文章可以有多个标签，一个标签也可以标记多篇文章（多对多关系）
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True)
    content = models.TextField("内容")
    create_date = models.DateTimeField("创建日期",auto_now_add=True)
    pub_date = models.DateTimeField("发布日期",auto_now=True)
    origin = models.URLField("来源",null=True,blank=True)
    is_from = models.CharField("来自", max_length=1, default='Y', choices=(('Y','yuanchuang'),('Z','zhuanzai')))
    view_count = models.IntegerField("访问量统计", default=0)
    vote_count = models.IntegerField("支持量统计", default=0)
    comment_count = property(lambda self: self.comment_set.count())
    is_yuan = property(lambda self: self.is_from == u'Y')
    is_zhuan = property(lambda self: self.is_from == u'Z')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering=['-pub_date']
    
    @property
    def pub_date_delta(self):
        d = timezone.localtime(self.pub_date)
        date = datetime.datetime(d.year,d.month,d.day,d.hour,d.minute, d.second)
        return utils.getTimeDelta(date)

    @property
    def comments(self):
        self.cmlist = []
        def com2dict(c):
            d = {}
            d['comm'] = c
            d['list'] = []
            return d
        def recur(objs, t, l):
            if t > 50:
                return
            for c in objs.all():
                d = com2dict(c)
                l.append(d)
                #print t*"  ", c.id, c.content
                if c.comment_set.count() > 0:
                    recur(c.comment_set, t+1, d['list'])
        for c in self.comment_set.filter(reply=None):
            #print c.id, c.content
            d = com2dict(c)
            self.cmlist.append(d)
            recur(c.comment_set, 0, d['list'])
        return self.cmlist

class Comment(models.Model):
    user_name = models.CharField('用户', max_length=32)
    email = models.EmailField("E-mail", blank=True)
    content = models.CharField("评论", max_length=64)
    create_date = models.DateTimeField("创建日期",auto_now_add=True)
    vote_count = models.IntegerField(default=0)
    #recursion
    reply = models.ForeignKey("self", null=True, blank=True, verbose_name="回复")
    #一篇文章有多条评论（多对一关系）
    article = models.ForeignKey(Article, null=True, blank=True, verbose_name="文章")
    
    class Meta:
        ordering=['-create_date']

    def __unicode__(self):
        return self.content

    @property
    def pub_date_delta(self):
        d = timezone.localtime(self.create_date)
        date = datetime.datetime(d.year,d.month,d.day,d.hour,d.minute, d.second)
        return utils.getTimeDelta(date)


