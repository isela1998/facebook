from crum import get_current_user, get_current_request
from mf.user.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone 
from datetime import date
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
from mf.models import BaseModel
from django.utils.dateparse import parse_datetime
import pytz

class Product_group(models.Model):
    name = models.CharField(max_length=10, verbose_name='Grupo', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Grupo de Productos'
        verbose_name_plural = 'Grupo de Productos'
        ordering = ['id']

class Type_debts(models.Model):
    name = models.CharField(max_length=10, verbose_name='Cobrar/Pagar', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipos de cuentas'
        verbose_name_plural = 'Tipo de cuenta'
        ordering = ['id']

class Type_services(models.Model):
    name = models.CharField(max_length=10, verbose_name='Servicio', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipos de servicios'
        verbose_name_plural = 'Tipo de servicio'
        ordering = ['id']

class Id_Type(models.Model):
    identity = models.CharField(max_length=10, verbose_name='Identificación', unique=True)

    def __str__(self):
        return self.identity

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de identificación'
        verbose_name_plural = 'Tipos de identificación'
        ordering = ['id'] 

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Categoría', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']

class Method_pay(models.Model):
    name = models.CharField(max_length=150, verbose_name='Método de Pago', unique=True)
    type_symbol = models.CharField(max_length=150, verbose_name='Abreviación/Símbolo')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de pago'
        ordering = ['id']

class Type_product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Tipo', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['id']

class Providers(models.Model):
    names = models.CharField(max_length=255, verbose_name="Razón Social")
    identity = models.ForeignKey(Id_Type, default='1', on_delete=models.PROTECT, verbose_name="Identificación")
    ci = models.CharField(max_length=50, verbose_name="RIF")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    contact = models.CharField(max_length=20, verbose_name="Contacto")

    def __str__(self):
        provider = self.names + ' (' + self.identity.identity + '-' + self.ci + ')' + ' ' + self.address
        return provider
    
    def toJSON(self):
        item = model_to_dict(self)
        item['identity'] = self.identity.toJSON()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

class Product(models.Model):
    code = models.CharField(max_length=150, verbose_name='Código', unique=True)
    product_group = models.ForeignKey(Product_group, on_delete=models.PROTECT, verbose_name="Grupo")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoría")
    type_product = models.ForeignKey(Type_product, on_delete=models.PROTECT, verbose_name="Tipo")
    product = models.CharField(max_length=150, verbose_name='Producto')
    cost = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Precio|Costo")
    price = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Precio sin IVA")
    price_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Precio|Venta")
    gain = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Ganancia")
    price_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Bs.")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad" )
    image = models.FileField(upload_to='Products', default="Products/empty.png", null=True, blank=True)
    date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name='Fecha de actualización')

    def __str__(self):
        return '{}.{}.{}'.format(self.brand, self.product, self.type_product.name)
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['date'])
        item['product_group'] = self.product_group.toJSON()
        item['category'] = self.category.toJSON()
        item['type_product'] = self.type_product.toJSON()
        item['cost'] = format(self.cost, '.2f')
        item['price'] = format(self.price, '.2f')
        item['price_dl'] = format(self.price_dl, '.2f')
        item['price_bs'] = format(self.price_bs, '.2f')
        item['gain'] = format(self.gain, '.2f')
        item['image'] = str(self.image)
        return item
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Cliente')
    identity = models.ForeignKey(Id_Type, default='1', on_delete=models.PROTECT, verbose_name="Identificación")
    ci = models.CharField(max_length=50, unique=True, verbose_name='CI/RIF')
    address = models.CharField(max_length=180, verbose_name='Dirección')
    contact = models.CharField(max_length=50, verbose_name='Teléfono')

    def __str__(self):
        client = self.names + ' ' + self.identity.identity + '-' + self.ci
        return client

    def toJSON(self):
        item = model_to_dict(self)
        item['identity'] = self.identity.toJSON()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Facilitator(models.Model):
    names = models.CharField(max_length=150, verbose_name='Facilitador')
    identity = models.ForeignKey(Id_Type, default='1', on_delete=models.PROTECT, verbose_name="Identificación")
    ci = models.CharField(max_length=50, unique=True, verbose_name='CI/RIF')
    contact = models.CharField(max_length=50, verbose_name='Teléfono')

    def __str__(self):
        client = self.names + ' ' + self.identity.identity + '-' + self.ci
        return client

    def toJSON(self):
        item = model_to_dict(self)
        item['identity'] = self.identity.toJSON()
        return item

    class Meta:
        verbose_name = 'Facilitador'
        verbose_name_plural = 'Facilitadores'
        ordering = ['id']

class Sale(models.Model):
    datejoined = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    invoice_number = models.CharField(max_length=255, default='00000000', verbose_name="Nº Venta")
    cli = models.ForeignKey(Client, on_delete=models.PROTECT)
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    total_sale = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Total Sin/Descuento')
    total_sale_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Total $$ Sin/Descuento')
    total_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    iva = models.DecimalField(default='16%', max_digits=30, decimal_places=2)
    type_sale = models.CharField(max_length=25, verbose_name='Método')
    discount = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    discount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    desc_discount = models.CharField(default='No aplica', max_length=250, verbose_name='Nota')
    method_pay = models.ForeignKey(Method_pay, on_delete=models.PROTECT, blank=True, null=True, related_name='method_pays', verbose_name="Método de pago (1)")
    method_pay1 = models.ForeignKey(Method_pay, on_delete=models.PROTECT, blank=True, null=True, related_name='method_pays1', verbose_name="Método de pago (2)")
    method_pay2 = models.ForeignKey(Method_pay, on_delete=models.PROTECT, blank=True, null=True, related_name='method_pays2', verbose_name="Método de pago (3)")
    received = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Entrada (1)')
    received1 = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Entrada (2)')
    received2 = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Entrada (3)')
    exchange = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Cambio')
    exchange1 = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Cambio')
    exchange2 = models.DecimalField(default=0, max_digits=100, decimal_places=2, verbose_name='Cambio')
    description = models.CharField(default="Sin observaciones", max_length=250, verbose_name='Nota')
    rate = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    order = models.CharField(max_length=255, default='00000000', verbose_name="Número de guía")
    status = models.IntegerField(default=0)

    def __str__(self):
        # return self.cli.names
        return '{}.{}'.format(self.cli.names, self.cli.ci)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['discount_dl'] = format(self.discount_dl, '.2f')
        item['received'] = format(self.received, '.2f')
        item['received1'] = format(self.received1, '.2f')
        item['received2'] = format(self.received2, '.2f')
        item['exchange'] = format(self.exchange, '.2f')
        item['exchange1'] = format(self.exchange1, '.2f')
        item['exchange2'] = format(self.exchange2, '.2f')
        item['total'] = format(self.total, '.2f')
        item['total_sale'] = format(self.total_sale, '.2f')
        item['total_sale_dl'] = format(self.total_sale_dl, '.2f')
        item['total_dl'] = format(self.total_dl, '.2f')
        item['method_pay'] = self.method_pay.toJSON()
        item['method_pay1'] = self.method_pay1.toJSON()
        item['method_pay2'] = self.method_pay2.toJSON()
        item['rate'] = format(self.rate, '.2f')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_product_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto en Bs.')
    price_product_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto en $')
    price = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto S/IVA')
    quantity = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal S/IVA')
    subtotal_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal $ S/IVA')
    gain = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Ganancia")
    sub = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal C/IVA')
    rate = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Tasa $ Calculada')

    def __str__(self):
        # return '{}.{}.{}'.format(self.prod.brand, self.prod.product, self.prod.type_product.name)
        return self.prod.name
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['price_product_bs'] = format(self.price_product_bs, '.2f')
        item['price_product_dl'] = format(self.price_product_dl, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['subtotal_dl'] = format(self.subtotal_dl, '.2f')
        item['gain'] = format(self.gain, '.2f')
        item['sub'] = format(self.sub, '.2f')
        item['rate'] = format(self.rate, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class Dolar(models.Model):
    dolar = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)

    def __str__(self):
        return self.dolar
    
    def toJSON(self):
        item = model_to_dict(self)
        item['dolar'] = format(self.dolar, '.2f')
        return item

class Requested(models.Model):
    name = models.CharField(max_length=150, verbose_name='Producto', unique=True)
    description = models.CharField(max_length=200, verbose_name='Descripción')

    def __str__(self):
        return '{}.{}'.format(self.name, self.description) 

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Productos Solicitados'
        verbose_name_plural = 'Productos Solicitados'
        ordering = ['id']

class Permisology(models.Model):
    name = models.CharField(max_length=255, verbose_name='Permiso')
    description = models.CharField(max_length=180, verbose_name='Descripción')
    day = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name='Fecha de pago')
    color = models.CharField(max_length=250, default='#007bff', verbose_name='Color')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Permisos y Eventos'
        verbose_name_plural = 'Permisos y Eventos'
        ordering = ['id']

class Debts(models.Model):
    type_debts = models.ForeignKey(Type_debts, default='1', on_delete=models.PROTECT, verbose_name="Cobrar/Pagar")
    client = models.CharField(max_length=255, verbose_name='Proveedor/Cliente')
    description = models.CharField(max_length=255, verbose_name='Descripción')
    rate = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Tasa(Bs.)")
    start_date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name='Fecha de Inicio')
    end_date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name='Fecha límite')
    dollars = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto ($)")
    bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto (Bs.)")

    def __str__(self):
        return '{}.{}'.format(self.client, self.description)

    def toJSON(self):
        item = model_to_dict(self)
        item['type_debts'] = self.type_debts.toJSON()
        item['rate'] = format(self.rate, '.2f')
        item['dollars'] = format(self.dollars, '.2f')
        item['bs'] = format(self.bs, '.2f')
        return item

    class Meta:
        verbose_name = 'Cuenta por Cobrar/Pagar'
        verbose_name_plural = 'Cuentas por Cobrar/Pagar'
        ordering = ['id']

class Expenses(models.Model):
    date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    concept = models.CharField(max_length=255, verbose_name="Concepto")
    amount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto($)")
    amount_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto(Bs.)")

    def __str__(self):
        return self.concept
    
    def toJSON(self):
        item = model_to_dict(self)
        item['amount_dl'] = format(self.amount_dl, '.2f')
        item['amount_bs'] = format(self.amount_bs, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['id']

class Shopping(models.Model):
    date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    concept = models.CharField(max_length=255, verbose_name="Concepto")
    amount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto($)")
    amount_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto(Bs.)")

    def __str__(self):
        return self.concept
    
    def toJSON(self):
        item = model_to_dict(self)
        item['amount_dl'] = format(self.amount_dl, '.2f')
        item['amount_bs'] = format(self.amount_bs, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class Earnings(models.Model):
    date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    concept = models.CharField(max_length=255, verbose_name="Concepto")
    amount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto($)")
    amount_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto(Bs.)")

    def __str__(self):
        return self.concept
    
    def toJSON(self):
        item = model_to_dict(self)
        item['amount_dl'] = format(self.amount_dl, '.2f')
        item['amount_bs'] = format(self.amount_bs, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Ganancia'
        verbose_name_plural = 'Ganancias'
        ordering = ['id']

class BankAccounts(models.Model):
    bank = models.CharField(max_length=255, verbose_name="Nombre del Banco")
    accountHolder = models.CharField(max_length=255, verbose_name="Titular de la Cuenta")
    holderId = models.CharField(max_length=255, verbose_name="Cédula/RIF Titular")
    accountNumber = models.CharField(max_length=255, verbose_name="Número de Cuenta")

    def __str__(self):
        bankAccount = self.bank + ' ' + self.accountHolder + '(' + self.holderId + ')' + ' ' + self.accountNumber
        return bankAccount
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cuenta Bancaria'
        verbose_name_plural = 'Cuentas Bancarias'
        ordering = ['id']  

class BankTransfers(models.Model):
    pay_date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    bank = models.ForeignKey(BankAccounts, on_delete=models.PROTECT, verbose_name="Banco")
    referenceNumber = models.CharField(max_length=30, verbose_name="Número de Referencia")
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Monto")
    description = models.CharField(max_length=180, verbose_name='Notas y/o Descripción', blank=True, null=True)
    image = models.FileField(upload_to='Cap_Banktransfers', null=True, blank=True)

    def __str__(self):
        return self.referenceNumber

    def toJSON(self):
        item = model_to_dict(self)
        item['bank'] = self.bank.toJSON()
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Transferencias Bancarias'
        ordering = ['id']

class CancelledInvoices(models.Model):
    pay_date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    provider = models.ForeignKey(Providers, on_delete=models.PROTECT, verbose_name="Proveedor")
    quantity = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Cantidad ($$)")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    image = models.FileField(upload_to='Cap_Facturas', null=True, blank=True)

    def __str__(self):
        cancelledInv = self.pay_date  + ' '  + self.provider
        return cancelledInv

    def toJSON(self):
        item = model_to_dict(self)
        item['provider'] = self.provider.toJSON()
        item['quantity'] = format(self.quantity, '.2f')
        return item

    class Meta:
        verbose_name = 'Factura Cancelada'
        verbose_name_plural = 'Facturas Canceladas'
        ordering = ['id']

class CompanyInfo(models.Model):
    name = models.CharField(max_length=225, verbose_name="Razón Social")
    rif = models.CharField(max_length=225, verbose_name="RIF")

    def __str__(self):
        return '{}.{}'.format(self.name, self.rif)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Información de la Empresa"
        ordering = ['id']

class CompanySedes(models.Model):
    rif = models.CharField(max_length=225, verbose_name="RIF")
    address = models.CharField(max_length=225, verbose_name="Dirección Fiscal")
    postal_zone = models.CharField(max_length=5, verbose_name="Zona Postal")
    phone = models.CharField(max_length=100, verbose_name="Telefono(s)")
    email = models.CharField(max_length=100, verbose_name="Correo")

    def __str__(self):
        return self.address
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Información de las Sedes"
        ordering = ['id']

class Budget(models.Model):
    budget_number = models.CharField(max_length=255, default='00000000', verbose_name="Presupuesto Nº")
    cli = models.ForeignKey(Client, on_delete=models.PROTECT)
    datejoined = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    subtotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    iva = models.DecimalField(default='16%', max_digits=30, decimal_places=2)
    type_sale = models.CharField(max_length=25, verbose_name='Presupuesto')
    discount = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    discount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    desc_discount = models.CharField(default='No aplica', max_length=250, verbose_name='Nota')
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    total_sale = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Total Sin/Descuento')
    total_sale_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Total $$ Sin/Descuento')
    total_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    description = models.CharField(max_length=250, verbose_name='Nota')
    rate = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)

    def __str__(self):
        return self.budget_number

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['discount_dl'] = format(self.discount_dl, '.2f')
        item['total'] = format(self.total, '.2f')
        item['total_sale'] = format(self.total_sale, '.2f')
        item['total_sale_dl'] = format(self.total_sale_dl, '.2f')
        item['total_dl'] = format(self.total_dl, '.2f')
        item['rate'] = format(self.rate, '.2f')
        item['det'] = [i.toJSON() for i in self.detbudget_set.all()]
        return item
    
    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['id']

class DetBudget(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_product_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto en Bs.')
    price_product_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto en $')
    price = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio del Producto S/IVA')
    quantity = models.IntegerField(default=0)
    sub = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal C/IVA')
    subtotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal S/IVA')
    subtotal_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Subtotal $ S/IVA')
    rate = models.DecimalField(default=0.00, max_digits=30, decimal_places=22, verbose_name='Tasa $ Calculada')


    def __str__(self):
        # return '{}.{}.{}'.format(self.prod.brand, self.prod.product, self.prod.type_product.name)
        return self.prod.name
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['budget'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['price_product_bs'] = format(self.price_product_bs, '.2f')
        item['price_product_dl'] = format(self.price_product_dl, '.2f')
        item['sub'] = format(self.sub, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['subtotal_dl'] = format(self.subtotal_dl, '.2f')
        item['rate'] = format(self.rate, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Presupuesto'
        verbose_name_plural = 'Detalle de Presupuestos'
        ordering = ['id']

class Payments(models.Model):
    pay_date = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    provider = models.CharField(max_length=255, verbose_name="Proveedor/Cliente")
    quantity = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Abono|$$")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    image = models.FileField(upload_to='Cap_Payments', null=True, blank=True)

    def __str__(self):
        payment = self.pay_date + ' ' + self.provider
        return payment

    def toJSON(self):
        item = model_to_dict(self)
        item['quantity'] = format(self.quantity, '.2f')
        return item

    class Meta:
        verbose_name = 'Abono de Factura'
        verbose_name_plural = 'Abonos de Facturas'
        ordering = ['id']

class DollarHistory(models.Model):
    datejoined = models.CharField(default=date.today().strftime('%Y-%m-%d'), max_length=30, verbose_name="Fecha")
    rate_dolar1 = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name="Tasa general")

    def __str__(self):
        dolar = self.datejoined + ' ' + 'Tasa general: ' + self.rate_dolar1 
        return dolar

    def toJSON(self):
        item = model_to_dict(self)
        item['rate_dolar1'] = format(self.rate_dolar1, '.2f')
        return item

    class Meta:
        verbose_name = 'Historial (Dólar)'
        verbose_name_plural = 'Historial (Dólar)'
        ordering = ['id']

class HistoryOperations(models.Model):
    datejoined = models.CharField(default=date.today().strftime('%Y-%m-%d'), max_length=30, verbose_name="Fecha")
    userSession = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario")
    description = models.CharField(max_length=2255, verbose_name='Descripción')

    def __str__(self):
        history = self.date_joined + ' (' + self.userSession + '): ' + self.description
        return history

    def toJSON(self):
        item['userSession'] = self.userSession.toJSON()
        return item
    
    class Meta:
        verbose_name = 'Historial de Operaciones'
        verbose_name_plural = 'Historial de Operaciones'
        ordering = ['id']

class Invoices(models.Model):
    number_invoice = models.CharField(max_length=255, default='00000000', verbose_name="Compra Nº")
    datejoined = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    provider = models.ForeignKey(Providers, on_delete=models.PROTECT, verbose_name="Proveedor")
    facilitator = models.ForeignKey(Facilitator, on_delete=models.PROTECT, verbose_name="Facilitador")
    subtotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    expenses = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)

    def __str__(self):
        invoice = self.datejoined + ' ' + self.provider.names + ' ' + self.total
        return invoice
    
    def toJSON(self):
        item = model_to_dict(self)
        item['facilitator'] = self.facilitator.toJSON()
        item['provider'] = self.provider.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['expenses'] = format(self.expenses, '.2f')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJSON() for i in self.detinvoices_set.all()]
        return item

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['id']

class DetInvoices(models.Model):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    code = models.CharField(max_length=150, verbose_name='Código')
    category = models.CharField(max_length=150, verbose_name='Categoria')
    type_product = models.CharField(max_length=150, verbose_name='Tipo de Producto')
    product = models.CharField(max_length=150, verbose_name='Producto')
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Total')
    quantity = models.IntegerField(default=0, verbose_name="Cantidad" )
    unit_price = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio|Unitario')
    shipment = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='%|Envío')
    gain = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='%|Ganancia')
    final_price = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Precio|Final')

    def __str__(self):
        return 'Model Details Invoices'

    def toJSON(self):
        item = model_to_dict(self, exclude=['invoice'])
        item['total'] = format(self.total, '.2f')
        item['unit_price'] = format(self.unit_price, '.2f')
        item['shipment'] = format(self.shipment, '.2f')
        item['gain'] = format(self.gain, '.2f')
        item['final_price'] = format(self.final_price, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalle de Facturas'
        ordering = ['id']

class Services(models.Model):
    datejoined = models.DateField(max_length=10, default=date.today().strftime('%Y-%m-%d'), verbose_name="Fecha")
    type_service = models.ForeignKey(Type_services, on_delete=models.PROTECT, verbose_name="Servicio")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad" )
    amount_dl = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Monto|$')
    amount_bs = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, verbose_name='Monto|Bs.')
    description = models.CharField(max_length=250, verbose_name='Descripción')

    def __str__(self):
        return self.datejoined + ' ' + self.type_service.name + ' ' + self.amount_dl

    def toJSON(self):
        item = model_to_dict(self)
        item['type_service'] = self.type_service.toJSON()
        item['amount_dl'] = format(self.amount_dl, '.2f')
        item['amount_bs'] = format(self.amount_bs, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']


































