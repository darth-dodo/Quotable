from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^(\w+)/$', views.modes),
    url(r'^imdb/(\w+)/', views.imdb_worker),
     url(r'^goodreads/(\w+)/', views.hello),

]
