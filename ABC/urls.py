from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^login_view$', views.login_view, name='login_view'),
    url(r'^logout_view$', views.logout_view, name='logout_view'),

    url(r'new_item/$', views.new_item, name='new_item'),
    url(r'add_item/$', views.add_item, name='add_item'),
    url(r'^delete_item/(?P<item_id>[0-9]*)/$', views.delete_item, name='delete_item'),
    url(r'^item/(?P<item_id>[0-9]*)/$', views.item, name='item'),
    url(r'items/$', views.items, name='items'),
    url(r'^autocomplete_item/$', views.autocomplete_item, name='autocomplete_item'),
    url(r'^item_info/$', views.item_info, name='item_info'),

    url(r'new_provider/$', views.new_provider, name='new_provider'),
    url(r'add_provider/$', views.add_provider, name='add_provider'),
    url(r'delete_provider/(?P<provider_id>[0-9]*)/$', views.delete_provider, name='delete_provider'),
    url(r'providers/$', views.providers, name='providers'),
    url(r'^provider_info/$', views.provider_info, name='provider_info'),

    url(r'new_customer/$', views.new_customer, name='new_customer'),
    url(r'add_customer/$', views.add_customer, name='add_customer'),
    url(r'delete_customer/(?P<customer_id>[0-9]*)/$', views.delete_customer, name='delete_customer'),
    url(r'report_customers/$', views.report_customers, name='report_customers'),
    url(r'customers/$', views.customers, name='customers'),
    url(r'^autocomplete_customer/$', views.autocomplete_customer, name='autocomplete_customer'),
    url(r'^customer_info/$', views.customer_info, name='customer_info'),

    url(r'new_order/$', views.new_order, name='new_order'),
    url(r'add_order/$', views.add_order, name='add_order'),
    url(r'delete_order/(?P<order_id>[0-9]*)/$', views.delete_order, name='delete_order'),
    url(r'orders/$', views.orders, name='orders'),
    url(r'^order_details_info/$', views.order_details_info, name='order_details_info'),

    url(r'new_invoice/$', views.new_invoice, name='new_invoice'),
    url(r'add_invoice/$', views.add_invoice, name='add_invoice'),
    url(r'delete_invoice/(?P<invoice_id>[0-9]*)/$', views.delete_invoice, name='delete_invoice'),
    url(r'invoices/$', views.invoices, name='invoices'),

    url(r'new_event/$', views.new_event, name='new_event'),
    url(r'add_event/$', views.add_event, name='add_event'),
    url(r'delete_event/(?P<event_id>[0-9]*)/$', views.delete_event, name='delete_event'),
    url(r'events/$', views.events, name='events'),

    url(r'new_task/$', views.new_task, name='new_task'),
    url(r'add_task/$', views.add_task, name='add_task'),
    url(r'delete_task/(?P<task_id>[0-9]*)/$', views.delete_task, name='delete_task'),
    url(r'tasks/$', views.tasks, name='tasks'),

    url(r'master_tables/$', views.master_tables, name='master_tables'),
    url(r'new_delivery_type/$', views.new_delivery_type, name='new_delivery_type'),
    url(r'add_delivery_type/$', views.add_delivery_type, name='add_delivery_type'),
    url(r'delete_delivery_type/(?P<delivery_type_id>[0-9]*)/$', views.delete_delivery_type, name='delete_delivery_type'),
    url(r'^delivery_type_info/$', views.delivery_type_info, name='delivery_type_info'),
    url(r'new_payment_type/$', views.new_payment_type, name='new_payment_type'),
    url(r'add_payment_type/$', views.add_payment_type, name='add_payment_type'),
    url(r'delete_payment_type/(?P<payment_type_id>[0-9]*)/$', views.delete_payment_type, name='delete_payment_type'),
    url(r'new_vat_type/$', views.new_vat_type, name='new_vat_type'),
    url(r'add_vat_type/$', views.add_vat_type, name='add_vat_type'),
    url(r'delete_vat_type/(?P<vat_type_id>[0-9]*)/$', views.delete_vat_type, name='delete_vat_type'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)