from django.db import models
from django.utils import timezone


class VatType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    rate = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(default='')
    cost = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(default='')
    cost = models.FloatField(default=0, null=True)
    days = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Customer(models.Model):
    cif = models.CharField(max_length=25, blank=True)
    company_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.IntegerField(default=0, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    fax = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(default=None, null=True)
    web = models.URLField(default='http://', blank=True)
    notes = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.company_name


class Provider(models.Model):
    name = models.CharField(max_length=50,unique=True)
    contact_name = models.CharField(max_length=100)
    cif = models.CharField(max_length=25, unique=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.IntegerField(default=0, null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    email = models.EmailField(default=None)
    web = models.URLField(default='http://', blank=True)
    notes = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(default='')
    stock = models.IntegerField(default=0)
    cost_price = models.FloatField(default=0, blank=True)
    retail_price = models.FloatField(default=0, blank=True)
    notes = models.TextField(default='', null=True, blank=True)
    image1 = models.ImageField(upload_to='items', blank=True)
    image2 = models.ImageField(upload_to='items', blank=True)
    image3 = models.ImageField(upload_to='items', blank=True)
    thumbnail = models.ImageField(upload_to='items')
    provider = models.ForeignKey(Provider, null=True)
    vat_type = models.ForeignKey(VatType, null=True)

    @classmethod
    def create(cls, name, description, price, thumbnail):
        item = cls(name=name, description=description, retail_price=price, thumbnail=thumbnail)
        return item

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default='')
    date = models.DateTimeField(default=timezone.datetime.now)
    location = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    notice_date = models.DateTimeField(default=timezone.datetime.now, null=True, blank=True)
    done = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.CharField(max_length=20,unique=True)
    date = models.DateTimeField(default=timezone.datetime.now)
    delivery_date = models.DateTimeField(default=timezone.datetime.now)
    state = models.CharField(max_length=50)
    notes = models.TextField(default='', blank=True)
    tax_base = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    customer = models.ForeignKey(Customer)
    delivery_cost = models.FloatField(default=0)
    payment_cost = models.FloatField(default=0)
    document = models.FileField(upload_to='items', default=None, blank=True)
    delivery_days = models.PositiveSmallIntegerField(default=0)
    delivery_type = models.ForeignKey(DeliveryType, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class OrderDetail(models.Model):
    item = models.ForeignKey(Item)
    item_name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.FloatField(default=0)
    quantity = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    notes = models.TextField(default='')
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.order.number + "|" + self.item.name


class Invoice(models.Model):
    number = models.CharField(max_length=20,unique=True)
    date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    state = models.CharField(max_length=50)
    notes = models.TextField(default='')
    tax_base = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.IntegerField(default=0)
    document = models.FileField(upload_to='invoices',default=None)
    payment_type = models.ForeignKey(PaymentType)
    order = models.ForeignKey(Order)
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.number


class InvoiceDetail(models.Model):
    item = models.ForeignKey(Item)
    item_name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.FloatField(default=0)
    quantity = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    notes = models.TextField(default='')
    invoice = models.ForeignKey(Invoice)

    def __str__(self):
        return self.invoice.number + "|" + self.item.name


class Task(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(default='')
    date = models.DateField(default=timezone.datetime.now)
    start_date = models.DateTimeField(default=timezone.datetime.now, null=True, blank=True)
    finish_date = models.DateTimeField(default=timezone.datetime.now, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True)
    state = models.CharField(max_length=50)
    notice = models.TextField(default='', null=True, blank=True)
    notice_date = models.DateTimeField(default=timezone.datetime.now, null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20,unique=True,null=False)
    password = models.CharField(max_length=100,null=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.IntegerField(default=0)
    phone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    logo_image = models.ImageField(upload_to='company')
    email = models.EmailField(default=None)
    web = models.URLField(default='http://')

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name + "=" + self.value
