from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'items/$', views.items, name='items'),
    url(r'add_item/$', views.add_item, name='add_item'),
    url(r'^remove_item/(?P<item_id>[0-9]*)/$', views.remove_item, name='remove_item'),
    url(r'^item/(?P<item_id>[0-9]*)/$', views.item, name='item'),
    url(r'signin/$', views.signin, name='signin'),
    url(r'tasks/$', views.tasks, name='tasks')
]