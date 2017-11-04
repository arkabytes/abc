from django.contrib import admin

from .models import *

admin.site.register(DeliveryType)
admin.site.register(PaymentType)
admin.site.register(VatType)
admin.site.register(Customer)
admin.site.register(Provider)
admin.site.register(Item)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Option)