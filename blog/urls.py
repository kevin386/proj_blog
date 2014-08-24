from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
	url(r'page/(?P<index>\d{1,5})/$', 'page',name="articles_by_page"),
    url(r'art/(?P<id>\d{1,5})/$', 'article',name="article_by_id"),
    url(r'cat/(?P<id>\d{1,5})/(?P<index>\d{1,5})/$', 'category', name="articles_by_cat"),
    url(r'vote/(?P<id>\d{1,5})/$', 'vote', name='article_vote_url'),
    url(r'tag/(?P<id>\d{1,5})/(?P<index>\d{1,5})/$', 'tag', name='articles_by_tag'),
    url(r'aboutme/$', 'about_me', name="about_me"),
    url(r'search/(?P<index>\d{1,5})/$', 'search_articel', name="search_articel"),
    url(r'comment/(?P<id>\d{1,5})/$', 'submit_comment', name="submit_comment"),
)


