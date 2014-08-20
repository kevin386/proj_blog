#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response,get_list_or_404
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from blog.models import *
from blog.logic import *

def submit_comment(request,id):
    blog = Blog()
    errors = []
    content = request.POST.get('comment_content')
    user_name = request.POST.get('user_name')
    email = request.POST.get('email')
    if user_name and content:
        article = get_object_or_404(Article,id=id)
        com = Comment(user_name=user_name,email=email,content=content,article=article)
        com.save()
    return HttpResponseRedirect(reverse("article_by_id", kwargs={"id":id}))

def search_articel(request):
    blog = Blog()
    content = request.POST.get('search_content')
    articles = Article.objects.filter(title__icontains=content)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def about_me(request):
    blog = Blog()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def tag(request,id):
    blog = Blog()
    tag = get_object_or_404(Tag,id=id)
    articles = tag.article_set.all()
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
    articles = cat.article_set.all()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@page_view_analyze
def home(request):
    blog = Blog()
    articles = Article.objects.all()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
