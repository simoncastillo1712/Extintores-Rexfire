from django import forms
from django.contrib.auth.models import User
from .models import Categoria, Producto, Cliente, Proveedor, Vendedor

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'nombre',
            'descripcion'
        ]

        labels = {
            'nombre': 'Nombre de la categoria: ',
            'descripcion': 'Descripción: '
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'precio',
            'stock',
            'descripcion',
            'id_categoria',
            'imagen',
        ]

        labels = {
            'nombre': 'Nombre del Producto: ',
            'precio': 'Precio: ',
            'stock': 'Stock: ',
            'descripcion': 'Descripción: ',
            'id_categoria': 'Categoría',
            'imagen': 'Imagen del producto',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'rut_cliente',
            'razon_social',
            'direccion',
            'telefono',
            'email',
            'contacto_empresa',
            'fecha_ultimo_trabajo',
        ]

        labels ={
            'rut_cliente': 'Rut: ',
            'razon_social':'Nombre o Razón Social: ',
            'direccion':'Dirección: ',
            'telefono' : 'Teléfono: ',
            'email':'Correo Electronico',
            'contacto_empresa': 'Contacto (en caso de ser empresa): ',
            'fecha_ultimo_trabajo': 'Fecha del último trabajo realizado: ',
        }

        widgets = {
            'rut_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ultimo_trabajo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }

        help_texts = {
            'fecha_ultimo_trabajo': 'Dejar en blanco si es un cliente nuevo, sin trabajos realizados aún.',
        }
        
    def clean_rut_cliente(self):
        rut = self.cleaned_data['rut_cliente']
        if len(rut) < 8:
            raise forms.ValidationError(
                'El Rut NO ES válido.')
        return rut
            
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
                'rut_proveedor',
                'nombre_proveedor',
                'direccion',
                'telefono',
                'email',          
            ]
            
        labels ={
            'rut_proveedor': 'Rut Proveedor: ',
            'nombre_proveedor':'Razón Social: ',
            'direccion':'Dirección: ',
            'telefono' : 'Teléfono: ',
            'email':'Correo Electronico'             
        }
        
        widgets = {
            'rut_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),            
        }
    def clean_rut_proveedor(self):
        rut = self.cleaned_data['rut_proveedor']
        if len(rut) < 8:
            raise forms.ValidationError(
                'El Rut NO ES válido.')
        return rut


class ClientePerfilForm(forms.ModelForm):
    """Formulario para que el cliente edite sus propios datos (sin RUT)."""
    class Meta:
        model = Cliente
        fields = ['razon_social', 'direccion', 'telefono', 'email']
        labels = {
            'razon_social': 'Nombre / Razón Social',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class VendedorForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuario de acceso', max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        help_text='Para que el vendedor pueda iniciar sesión y ver su propio perfil (cotizaciones, ventas, comisiones). Deja en blanco si no necesita acceso.',
    )
    password = forms.CharField(
        label='Contraseña', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text='Al editar, deja en blanco para no cambiar la contraseña actual.',
    )

    class Meta:
        model = Vendedor
        fields = ['nombre', 'rut', 'telefono', 'email', 'activo']
        labels = {
            'nombre': 'Nombre completo',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'activo': 'Vendedor activo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569 XXXX XXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if username:
            qs = User.objects.filter(username=username)
            if self.instance.pk and self.instance.user_id:
                qs = qs.exclude(pk=self.instance.user_id)
            if qs.exists():
                raise forms.ValidationError('Ese nombre de usuario ya está en uso.')
        return username

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '')
        password = cleaned.get('password', '')
        tiene_cuenta = bool(self.instance.pk and self.instance.user_id)
        if username and not password and not tiene_cuenta:
            self.add_error('password', 'Debes definir una contraseña para la nueva cuenta de acceso.')
        return cleaned