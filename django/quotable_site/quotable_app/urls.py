from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^(\w+)/$', views.modes),
    # url(r'^imdb/movies/(\w+)/$', views.get_title),
    # url(r'^imdb/$', views.imdb_worker),
    url(r'^imdb/(?P<media>[a-zA-Z0-9-_. ]+)/(?P<mode>[a-zA-Z0-9-_. ]+)/$', views.imdb_worker_para),
    url(r'^imdb/(?P<media>[a-zA-Z0-9-_. ]+)/(?P<mode>[a-zA-Z0-9-_. ]+)/(?P<title>[a-zA-Z0-9-_. ]+)/$', views.get_title),
    url(r'^goodreads/(\w+)/', views.hello),

]
