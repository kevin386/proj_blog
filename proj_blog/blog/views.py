#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response 
from django.http import Http404
from blog import models

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

class Image(object):
	def __init__(self,src="",href="#"):
		self.src = src
		self.href = href

class Blog(object):
	def __init__(self,host):
		self.name = "kevin' blog"
		self.keywards = u"小虫子,django,python"
		self.author = "kevin"
		self.description = u"这是一个python程序员的博客"
		self.zen = Zen()
		self.avatar = Image()
		self.showRequest = False

		self.zen.content = zen_content
		self.zen.author = zen_author
		self.avatar.src = "static/images/IMG_Ali_01447.jpg"
		self.categories = [Url(host=host, name=cat.name, href="cat/"+str(cat.id)) for cat in models.Category.objects.all()]
		self.ranks = None
		self.lastestComments = None
		self.pageView = models.PageView.objects.all()
		self.catNav = self.categories

class Url(object):
	def __init__(self,host="", name="",href="#"):
		self.name = name
		if host:
			if not href.startswith('/'):
				host += '/'
			href = "http://" + host + href
		self.href = href

class Article(object):
	def __init__(self, art=None, caption=True, host=""):
		if art:
			if art.is_from is 'Y' : 
				self.yuan = True 
			elif art.is_from is 'Z':
				self.zhuan = True
			self.day = art.pub_date.day
			self.date = '-'.join([str(art.pub_date.year),str(art.pub_date.month)])
			self.pulishTimeStamp = 2
			self.pulishDatetime = "2012-05-28 16:01"
			self.href = "art/" + str(art.id)
			self.title = art.title
			self.cat = Url(host=host, name=art.category.name, href="cat/" + str(art.category.id))
			self.commentCount = 0
			self.viewCount = art.view_count
			self.voteCount = art.vote_count
			if caption:
				self.caption = art.content[0:50] + "..."
			else:
				self.content = art.content

def article(request,id=0):
	host = request.META['HTTP_HOST']
	blog = Blog(host)
	try:
		art = models.Article.objects.get(id=id)
		article = Article(art, False, host)
		if int(id) - 1 >= 0:
			art = models.Article.objects.get(id=str((int(id))-1));
			preArticle = Url(host=host, name=art.title, href="art/" + str(art.id))
		if int(id) + 1 >= 0:
			art = models.Article.objects.get(id=str((int(id))+1))
			nextArticle = Url(host=host, name=art.title, href="art/" + str(art.id))
	except models.Article.DoesNotExist, e:
		raise Http404
	finally:
		pass
	return render_to_response('article.html', locals())

def category(request,id=0):
	host = request.META['HTTP_HOST']
	blog = Blog(host)
	try:
		articles = [Article(art, host) for art in models.Article.objects.get(category=id)]
	except models.Article.DoesNotExist, e:
		raise Http404
	finally:
		pass
	return render_to_response('article.html', locals())

def home(request):
	host = request.META['HTTP_HOST'];
	blog = Blog(host)
	try:
		articles = [Article(art, host) for art in models.Article.objects.all()]
	except models.Article.DoesNotExist, e:
		raise Http404
	finally:
		pass
	return render_to_response('index.html', locals())
