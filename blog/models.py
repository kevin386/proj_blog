#-*- coding:utf-8 -*-
from django.db import models
import datetime

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
    is_from = models.CharField("来自", max_length=1, default='Y', choices=(('Y','yuanchuang'),('Z','zhuanzai')))
    view_count = models.IntegerField("访问量统计", default=0)
    vote_count = models.IntegerField("支持量统计", default=0)
    comment_count = property(lambda self: self.comment_set.count())
    is_yuan = property(lambda self: self.is_from == u'Y')
    is_zhuan = property(lambda self: self.is_from == u'Z')
    def pub_date_delta():
        doc = "The pub_date_delta property."
        def fget(self):
            today = datetime.datetime.today()
            if today.year - self.pub_date.year > 0:
                self._delta = "%d年前" % (today.year - self.pub_date.year)
            elif today.month - self.pub_date.month > 0:
                self._delta = "%d个月前" % (today.month - self.pub_date.month)
            elif today.day - self.pub_date.day > 0:
                self._delta = "%d天前" % (today.day - self.pub_date.day)
            elif today.hour - self.pub_date.hour > 0:
                self._delta = "%d小时前" % (today.hour - self.pub_date.hour)
            elif today.minute - self.pub_date.minute > 0:
                self._delta = "%d分钟前" % (today.minute - self.pub_date.minute)
            else:
                self._delta = ""
            return self._delta
        def fset(self, value):
            self._delta = value
        def fdel(self):
            del self._delta
        return locals()
    pub_date_delta = property(**pub_date_delta())
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField("评论", max_length=64)
    #引用别人的评论，为其它评论的ID，保存为"1,2,3,4"
    references = models.IntegerField(default=0)
    #一篇文章有多条评论（多对一关系）
    article = models.ForeignKey(Article, verbose_name="文章")
    def __unicode__(self):
        return self.content
