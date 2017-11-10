from django.db import models


class VatType(models.Model):
    name = models.CharField(max_length=25,unique=True)
    rate = models.FloatField(default=0)

    def __str__(self):
        return self.name;


class PaymentType(models.Model):
    name = models.CharField(max_length=25,unique=True)
    description = models.TextField(default=None)
    cost = models.FloatField(default=0)

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=25,unique=True)
    description = models.TextField(default=None)
    cost = models.FloatField(default=0)
    days = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Customer(models.Model):
    cif = models.CharField(max_length=25,unique=True)
    company_name = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.IntegerField(default=0)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.EmailField(default=None)
    web = models.URLField(default='http://')
    notes = models.TextField(default=None)

    def __str__(self):
        return self.company_name


class Provider(models.Model):
    name = models.CharField(max_length=50,unique=True)
    contact_name = models.CharField(max_length=100)
    cif = models.CharField(max_length=25,unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.IntegerField(default=0)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.EmailField(default=None)
    web = models.URLField(default='http://')
    notes = models.TextField(default=None)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(default=None)
    stock = models.IntegerField(default=0)
    cost_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)
    notes = models.TextField(default=None,null=True)
    image1 = models.ImageField(upload_to='items')
    image2 = models.ImageField(upload_to='items')
    image3 = models.ImageField(upload_to='items')
    thumbnail = models.ImageField(upload_to='items')
    provider = models.ForeignKey(Provider,null=True)
    vat_type = models.ForeignKey(VatType,null=True)

    @classmethod
    def create(cls, name, description, price, thumbnail):
        item = cls(name=name, description=description, retail_price=price, thumbnail=thumbnail)
        return item

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(default=None)
    date = models.DateTimeField
    location = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer)
    provider = models.ForeignKey(Provider)
    notice_date = models.DateTimeField

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.CharField(max_length=20,unique=True)
    date = models.DateField
    delivery_date = models.DateField
    state = models.CharField(max_length=50)
    notes = models.TextField(default=None)
    tax_base = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    customer = models.ForeignKey(Customer)
    delivery_cost = models.FloatField(default=0)
    payment_cost = models.FloatField(default=0)
    document = models.FileField(upload_to='orders',default=None)
    delivery_days = models.PositiveSmallIntegerField
    delivery_type = models.ForeignKey(DeliveryType)
    payment_type = models.ForeignKey(PaymentType)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class OrderDetail(models.Model):
    item = models.ForeignKey(Item)
    item_name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    price = models.FloatField(default=0)
    quantity = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    notes = models.TextField(default=None)
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.order.number + "|" + self.item.name


class Invoice(models.Model):
    number = models.CharField(max_length=20,unique=True)
    date = models.DateField
    due_date = models.DateField
    state = models.CharField(max_length=50)
    notes = models.TextField(default=None)
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
    description = models.TextField(default=None)
    price = models.FloatField(default=0)
    quantity = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    notes = models.TextField(default=None)
    invoice = models.ForeignKey(Invoice)

    def __str__(self):
        return self.invoice.number + "|" + self.item.name


class Task(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(default=None)
    date = models.DateField
    start_date = models.DateTimeField
    finish_date = models.DateTimeField
    location = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer)
    provider = models.ForeignKey(Provider)
    order = models.ForeignKey(Order)
    state = models.CharField(max_length=50)
    notice = models.TextField(default=None)
    notice_date = models.DateTimeField

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
