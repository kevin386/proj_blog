#-*- coding:utf-8 -*-
import logging
from django.shortcuts import get_object_or_404,render_to_response,get_list_or_404
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
import time

from blog.models import *
from blog.logic import *

logger = logging.getLogger('worker')

FILTER_COMMENTS = [
    'www.larneda.org',
]

def filter_comment(comment):
    for flt_cmt in FILTER_COMMENTS:
        if comment in flt_cmt:
            return True
    return False

def submit_comment(request,id):
    blog = get_basic_output()
    article = get_object_or_404(Article,id=id)
    article_pre, article_next = get_pre_or_next_article(article.pub_date)
    user_name = request.POST.get('user_name')
    comment_content = request.POST.get('comment_content')
    email = request.POST.get('email')
    try:
        if len(user_name) == 0:
            raise InputException(u"至少让我知道您的称呼吧?")
        if len(comment_content) == 0:
            raise InputException(u"您似乎想吐槽点什么?")
        if filter_comment(comment_content):
            logger.error('filter_comment:\nREMOTE_ADDR: %s\nREMOTE_PORT: %s\nREQUEST_METHOD: %s\nREQUEST_URI: %s',
                request.META['REMOTE_ADDR'],
                request.META['REMOTE_PORT'],
                request.META['REQUEST_METHOD'],
                request.META['REQUEST_URI']
            )
            raise InputException(u"You are a very bad guy!!")
        com = Comment(user_name=user_name,email=email,content=comment_content,article=article)
        com.save()
        thanks = u"感谢您的吐槽与建议！"
        user_name = comment_content = email = None
    except InputException as e:
        error_input = e.value
    #return HttpResponseRedirect(reverse("article_by_id", kwargs={"id":id}))
    return render_to_response('article.html', locals(), context_instance=RequestContext(request))

def search_articel(request,index):
    search_content = request.POST.get('search_content', "")
    if search_content:
        search_content = search_content.strip()
        request.session['search_content'] = search_content
    else:
        search_content = request.session.get('search_content', "")
    blog,pages,page = get_basic_output(Article.objects.filter(title__icontains=search_content), index)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def about_me(request):
    blog = Blog()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def tag(request,id,index):
    tag = get_object_or_404(Tag,id=id)
    blog,pages,page = get_basic_output(tag.article_set.all(), index)
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

@page_view_analyze
def article(request,id):
    blog = get_basic_output()
    article = get_object_or_404(Article,id=id)
    article_pre, article_next = get_pre_or_next_article(article.pub_date)
    return render_to_response('article.html', locals(), context_instance=RequestContext(request))

def category(request,id,index):
    blog = Blog()
    cat = get_object_or_404(Category,id=id)
    pages = Paginator(cat.article_set.all(), PAGINATOR_SIZE)
    page = pages.page(index)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def page(request, index):
    blog,pages,page = get_basic_output(objects=Article.objects.all(), index=index, request=request, clear_content=True)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@page_view_analyze
def home(request):
    return page(request, 1)
