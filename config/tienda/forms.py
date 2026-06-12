from django import forms
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
            'email'            
        ]
        
        labels ={
            'rut_cliente': 'Rut: ',
            'razon_social':'Nombre o Razón Social: ',
            'direccion':'Dirección: ',
            'telefono' : 'Teléfono: ',
            'email':'Correo Electronico'             
        }
        
        widgets = {
            'rut_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),            
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