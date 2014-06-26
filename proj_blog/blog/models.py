#-*- coding:utf-8 -*-
from django.db import models

class PageView(models.Model):
	today = models.IntegerField("今日访问量")
	yesterday = models.IntegerField("昨天访问量")
	week = models.IntegerField("本周访问量")
	month = models.IntegerField("本月访问量")
	total = models.IntegerField("总访问量")
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
	create_date = models.DateField("创建日期",auto_now_add=True)
	pub_date = models.DateField("发布日期",auto_now=True)
	is_from = models.CharField("来自", max_length=1, default='Y')
	view_count = models.IntegerField("访问量统计", blank=True)
	vote_count = models.IntegerField("支持量统计", blank=True)
	def __unicode__(self):
		return self.title

class Comment(models.Model):
	content = models.CharField("评论", max_length=64)
	#引用别人的评论，为其它评论的ID，保存为"1,2,3,4"
	references = models.CharField("引用评论", max_length=128)
	#一篇文章有多条评论（多对一关系）
	article = models.ForeignKey(Article, verbose_name="文章")
	def __unicode__(self):
		return self.content
