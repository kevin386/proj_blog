from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'art/(?P<id>\d{1,5})/$', 'blog.views.article'),
    url(r'cat/(?P<id>\d{1,5})/$', 'blog.views.category'),
)


