from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.add),
    url(r'^books/add/book_review$', views.add_book),
    url(r'^books/add/review/(?P<id>\d+)$',views.add_review),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^review/delete/(?P<id>\d+)$', views.delete),
    url(r'^reviewer/(?P<id>\d+)$', views.reviewer),
]
