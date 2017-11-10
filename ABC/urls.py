from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'items/$', views.items, name='items'),
    url(r'^items/(?P<item_pos>[0-9]*)/$', views.items, name='items'),
    url(r'add_item/$', views.add_item, name='add_item'),
    url(r'^remove_item/(?P<item_id>[0-9]*)/$', views.remove_item, name='remove_item'),
    url(r'^item/(?P<item_id>[0-9]*)/$', views.item, name='item'),
    url(r'^new_item/$', views.new_item, name='new_item'),
    url(r'signin/$', views.signin, name='signin'),
    url(r'providers/$', views.providers, name='providers'),
    url(r'customers/$', views.customers, name='customers'),
    url(r'orders/$', views.orders, name='orders'),
    url(r'invoices/$', views.invoices, name='invoices'),
    url(r'events/$', views.events, name='events'),
    url(r'tasks/$', views.tasks, name='tasks')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)