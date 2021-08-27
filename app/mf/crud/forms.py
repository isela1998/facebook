from django.forms import *
from datetime import datetime
from mf.crud.models import *

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre de la categoría',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            )
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class TypeProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Type_product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre del tipo de producto',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class TypeServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Type_services
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre del tipo de servicio',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class MethodPayForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Method_pay
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre del tipo pago',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            ),
            'type_symbol': TextInput(
                attrs={
                    'placeholder': 'Ingrese la Abreviación o Símbolo',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
 
class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'code': TextInput(
                attrs={
                    'placeholder': 'Código',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            ),
            'category': Select(
                attrs={
                    'class': 'form-control medium',
            }),
            'product_group': Select(
                attrs={
                    'class': 'form-control medium',
            }),
            'type_product': Select(
                attrs={
                    'class': 'form-control medium',
            }),
            'product': TextInput(
                attrs={
                    'placeholder': 'Nombre del producto',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            ),
            'cost':TextInput(
                attrs={
                    'placeholder': 'Costo $$',
                    'class': 'form-control text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
            'price_dl':TextInput(
                attrs={
                    'placeholder': 'Venta $$',
                    'class': 'form-control text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
            'quantity':NumberInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control text-center',
                    'onclick': 'this.select()',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
            'image': FileInput(attrs={
                'class': 'form-control',
                'id': 'image'
            }),
        }
        exclude = ['date', 'price_bs', 'gain', 'price']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Nombres o Razon Social del cliente',
                    'autocomplete': 'off',
                    'class': 'form-control medium UpperCase',
                }
            ),
            'identity':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control medium',
                    'style': 'width: 100%; font-size: init!important;'
            }),
            'ci': TextInput(
                attrs={
                    'placeholder': 'Ej. 10203040 ó 10203040-5',
                    'autocomplete': 'off',
                    'class': 'form-control medium inputNumbers'
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Dirección de domicilio del cliente',
                    'autocomplete': 'off',
                    'class': 'form-control UpperCase medium'
                }
            ),
            'contact': TextInput(
                attrs={
                    'placeholder': 'Contacto del cliente',
                    'autocomplete': 'off',
                    'class': 'form-control medium inputNumbers'
                }
            ),
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class FacilitatorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Facilitator
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Nombres o Razon Social del cliente',
                    'autocomplete': 'off',
                    'class': 'form-control medium UpperCase',
                }
            ),
            'identity':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control medium',
                    'style': 'width: 100%; font-size: init!important;'
            }),
            'ci': TextInput(
                attrs={
                    'placeholder': 'Ej. 10203040 ó 10203040-5',
                    'autocomplete': 'off',
                    'class': 'form-control medium inputNumbers'
                }
            ),
            'contact': TextInput(
                attrs={
                    'placeholder': 'Contacto del cliente',
                    'autocomplete': 'off',
                    'class': 'form-control medium inputNumbers'
                }
            ),
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control larger select2',
                    'style': 'width: 100%'
            }),
            'datejoined': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'datejoined',
                    'data-target': '#datejoined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control text-center large',
                'autocomplete': 'off',
                'readonly': True,
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control large',
                'autocomplete': 'off'
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control text-center em-25 height-auto',
                'autocomplete': 'off'
            }),
            'method_pay':Select(
                attrs={
                    'class': 'form-control larger',
                    'style': 'width: 100%',
                    'value': 2,
            }),
            'method_pay1':Select(
                attrs={
                    'class': 'form-control larger',
                    'style': 'width: 100%',
                    'value': 1,
            }),
            'method_pay2':Select(
                attrs={
                    'class': 'form-control larger',
                    'style': 'width: 100%',
                    'value': 1,
            }),
            'description': Textarea(
                attrs={
                'class': 'form-control large UpperCase',
                'autocomplete': 'off',
            }),
            'discount':TextInput(
                attrs={
                    'placeholder': 'Cantidad a Descontar',
                    'class': 'form-control inputNumberFormat large',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'received':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'received1':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'received2':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'exchange':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'exchange1':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'exchange2':TextInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
            'desc_discount':TextInput(
                attrs={
                    'class': 'form-control large UpperCase',
                    'placeholder': 'Descripción del descuento',
                    'autocomplete': 'off'
                }
            ),
            'change':TextInput(
                attrs={
                    'class': 'form-control large text-center inputNumberFormat',
                    'placeholder': 'Pendiente por devolver...',
                    'autocomplete': 'off',
                    'value': '0,00',
                }
            ),
        }
        exclude = ['type_exchange','cancel', 'control_number']

class SearchProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'product':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control select2 UpperCase',
                    'style': 'width: 100%'
            }),
        }
        exclude = ['product', 'quantity', 'category', 'type_product', 'brand', 'description', 'price', 'price_dl', 'price_bs', 'date']

class RequestedForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        # self.fields['description'].widget.attrs['autocomplete'] = False

    class Meta:
        model = Requested
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre del producto',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            ),
            'description': Textarea(attrs={
                'placeholder': 'Descripción del Producto',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
  
class PermisologyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Permisology
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control UpperCase',
                    'placeholder': 'Título',
                    'autocomplete': 'off'
                }
            ),
            'description':Textarea(
                attrs={
                    'placeholder': 'Descripción del Permiso ó Evento',
                    'class': 'form-control',
                    'rows': 3,
                    'autocomplete': 'off'
                }
            ),
            'day': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': 'YYYY-MM-DD',
                    'id': 'day',
                    'data-target': '#day',
                    'data-toggle': 'datetimepicker'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class DebtsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Debts
        fields = '__all__'
        widgets = {
            'type_debts':Select(
                attrs={
                    'class': 'form-control medium UpperCase',
                    'style': 'width: 100%'
            }),
            'client':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control medium select2',
                    'style': 'width: 100%'
            }),
            'description':Textarea(
                attrs={
                    'placeholder': 'Descripción de la cuenta',
                    'class': 'form-control UpperCase',
                    'rows': 3,
                    'autocomplete': 'off'
                }
            ),
            'start_date':TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'start_date',
                    'data-target': '#start_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'end_date':TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'end_date',
                    'data-target': '#end_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'rate':TextInput(
                attrs={
                    'class': 'form-control inputNumberFormat',
                    'placeholder': 'Tasa en Bs.',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
            'dollars':TextInput(
                attrs={
                    'class': 'form-control inputNumberFormat',
                    'placeholder': 'Cantidad',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
        }
        exclude = ['bs']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ExpensesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concept'].widget.attrs['autofocus'] = True

    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'date': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': 'YYYY-MM-DD',
                    'id': 'date',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'concept': Textarea(
                attrs={
                    'placeholder': 'Descripción de la ganancia',
                    'class': 'form-control UpperCase',
                    'rows': 3,
                    'autocomplete': 'off'
                }
            ),
            'amount_dl': TextInput(
                attrs={
                    'placeholder': 'Cantidad ($)',
                    'class': 'form-control inputNumberFormat',
                    'autocomplete': 'off'
                }
            ),
        }
        exclude = ['amount_bs']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ShoppingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concept'].widget.attrs['autofocus'] = True

    class Meta:
        model = Shopping
        fields = '__all__'
        widgets = {
            'date': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': 'YYYY-MM-DD',
                    'id': 'date',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'concept': Textarea(attrs={
                'placeholder': 'Descripción de la ganancia',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
            'amount_dl': TextInput(
                attrs={
                    'placeholder': 'Cantidad ($)',
                    'class': 'form-control inputNumberFormat',
                    'autocomplete': 'off'
                }
            ),
        }
        exclude = ['amount_bs']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class EarningsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concept'].widget.attrs['autofocus'] = True

    class Meta:
        model = Earnings
        fields = '__all__'
        widgets = {
            'date': DateInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'amount_dl': TextInput(
                attrs={
                    'placeholder': 'Cantidad ($)',
                    'class': 'form-control inputNumberFormat',
                    'autocomplete': 'off'
                }
            ),
            'concept': Textarea(attrs={
                'placeholder': 'Descripción de la ganancia',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
        }
        exclude = ['amount_bs']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ProvidersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Providers
        fields = '__all__'
        widgets = {
            'names': TextInput(attrs={
                'placeholder': 'Nombres o Razon Social del Proveedor',
                'class': 'form-control UpperCase',
                'autocomplete': 'off'
            }),
            'identity':Select(
                attrs={
                    'autofocus': True,
                    'class': 'form-control medium',
                    'style': 'width: 100%; font-size: init!important;'
            }),
            'ci': TextInput(attrs={
                'placeholder': 'Ej. 10203040-5 ó 10203040-5',
                'class': 'form-control inputNumbers',
                'autocomplete': 'off'
            }),
            'address': TextInput(attrs={
                'placeholder': 'Dirección del Proveedor',
                'class': 'form-control UpperCase',
                'autocomplete': 'off'
            }),
            'contact': TextInput(attrs={
                'placeholder': 'Nº de teléfono',
                'class': 'form-control inputNumbers',
                'autocomplete': 'off'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class CancelledInvoicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CancelledInvoices
        fields = '__all__'
        widgets = {
            'pay_date': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'pay_date',
                    'data-target': '#pay_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'provider':Select(
                attrs={
                    'class': 'form-control medium',
                    'style': 'width: 100%'
            }),
            'quantity':TextInput(
                attrs={
                    'class': 'form-control inputNumberFormat',
                    'placeholder': 'Cantidad',
                    'autocomplete': 'off',
                    'onclick': 'this.select()',
                    'min': 0
                }
            ),
            'description': Textarea(attrs={
                'placeholder': 'Descripción del pago',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'id': 'image'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class CompanySedesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = CompanySedes
        fields = '__all__'
        widgets = {
            'rif':TextInput(
                attrs={
                    'placeholder': 'RIF de la empresa',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off',
                }
            ),
            'address':TextInput(
                attrs={
                    'placeholder': 'Ubicación de la sede',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off',
                }
            ),
            'postal_zone':TextInput(
                attrs={
                    'placeholder': 'Zona Postal',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'phone':TextInput(
                attrs={
                    'placeholder': 'Número de Télefono',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'email':TextInput(
                attrs={
                    'placeholder': 'Dirección de Correo Electronico',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off',
                }
            ),
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class BankAccountsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = BankAccounts
        fields = '__all__'
        widgets = {
            'bank': TextInput(attrs={
                'class': 'form-control UpperCase',
                'placeholder': 'Ingrese el nombre del banco',
                'autocomplete': 'off'
            }),
            'accountHolder': TextInput(attrs={
                'class': 'form-control UpperCase',
                'placeholder': 'Ingrese los datos del titular',
                'autocomplete': 'off'
            }),
            'holderId': TextInput(attrs={
                'class': 'form-control UpperCase',
                'placeholder': 'Ingrese la identificación del titular',
                'autocomplete': 'off'
            }),
            'accountNumber': TextInput(attrs={
                'class': 'form-control UpperCase',
                'placeholder': 'Ingrese el número de cuenta',
                'autocomplete': 'off'
            })
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class BankTransfersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = BankTransfers
        fields = '__all__'
        widgets = {
            'pay_date': DateInput(format='%Y-%m-%d',
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'pay_date',
                    'data-target': '#pay_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'bank':Select(attrs={
                'class': 'form-control medium',
                'style': 'width: 100%'
                }
            ),
            'referenceNumber':TextInput(attrs={
                'placeholder': 'Nº Referencia',
                'class': 'form-control',
                'autocomplete': 'off'
                }
            ),
            'total':TextInput(attrs={
                'placeholder': 'Ingrese el monto',
                'class': 'form-control inputNumberFormat',
                'autocomplete': 'off',
                'value': '0,00'
                }
            ),
            'description': Textarea(attrs={
                'placeholder': 'Ingresa la descripción del pago',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'id': 'image'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class PaymentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Payments
        fields = '__all__'
        widgets = {
           'pay_date': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'pay_date',
                    'data-target': '#pay_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'provider':TextInput(attrs={
                'placeholder': 'Datos del Proveedor/Cliente',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'quantity':TextInput(
                attrs={
                    'class': 'form-control inputNumberFormat',
                    'placeholder': 'Cantidad',
                    'onclick': 'this.select()',
                    'autocomplete': 'off',
                    'min': 0
                }
            ),
            'description': Textarea(attrs={
                'placeholder': 'Descripción del pago',
                'class': 'form-control UpperCase',
                'rows': 3,
                'autocomplete': 'off'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'id': 'image'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class InvoicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Invoices
        fields = '__all__'
        widgets = {
            'datejoined': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'datejoined',
                    'data-target': '#datejoined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'facilitator':Select(
                attrs={
                    'class': 'form-control',
            }),
            'provider':Select(
                attrs={
                    'class': 'form-control',
            }),
            'total':TextInput(
                attrs={
                    'placeholder': 'Totales',
                    'class': 'form-control larger text-center inputNumberFormat',
                    'autocomplete': 'off',
                    'value': '0,00',
                    'autofocus': True,
                }
            ),
            'description':TextInput(
                attrs={
                    'placeholder': 'Observaciones y/o notas',
                    'class': 'form-control UpperCase',
                    'autocomplete': 'off'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'datejoined': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': 'YYYY-MM-DD',
                    'id': 'datejoined',
                    'data-target': '#datejoined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'type_service': Select(
                attrs={
                    'class': 'form-control',
            }),
            'quantity': NumberInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control text-center',
                    'min': 0,
                    'value': '1',
                    'onclick': 'this.select()'
                }
            ),
            'amount_dl': TextInput(
                attrs={
                    'placeholder': 'Cantidad|$',
                    'class': 'form-control inputNumberFormat',
                    'autocomplete': 'off'
                }
            ),
            'amount_bs': TextInput(
                attrs={
                    'placeholder': 'Cantidad|Bs',
                    'class': 'form-control inputNumberFormat',
                    'autocomplete': 'off'
                }
            ),
            'description': Textarea(
                attrs={
                'class': 'form-control large UpperCase',
                'autocomplete': 'off',
                'placeholder': 'Descripción del servicio',
                'rows': 3
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
