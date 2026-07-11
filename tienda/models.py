# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    id_venta = models.OneToOneField('Venta', models.CASCADE, db_column='id_venta')
    numero_boleta = models.IntegerField()
    fecha_emision = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'boleta'

    def __str__(self):
        return self.numero_boleta
    
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
            return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut_cliente = models.CharField(unique=True, max_length=15)
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'
    
    def __str__(self):
        return self.razon_social

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.PositiveIntegerField()
    estado = models.CharField(max_length=9)
    id_proveedor = models.ForeignKey('Proveedor', models.SET_NULL, db_column='id_proveedor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compra'
    
    def __str__(self):
        return self.fecha


class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    id_compra = models.ForeignKey(Compra, models.CASCADE, db_column='id_compra', blank=True, null=True)
    id_producto = models.ForeignKey('Producto', models.RESTRICT, db_column='id_producto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_compra'
        
    def __str__(self):
        return self.id_detalle_compra


class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey('Venta', models.CASCADE, db_column='id_venta')
    id_producto = models.ForeignKey('Producto', models.RESTRICT, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    subtotal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalle_venta'
    
    def __str__(self):
        return self.id_detalle_venta


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_venta = models.OneToOneField('Venta', models.CASCADE, db_column='id_venta')
    numero_factura = models.IntegerField()
    fecha_emision = models.DateTimeField()
    id_cliente = models.ForeignKey(Cliente, models.RESTRICT, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factura'

    def __str__(self):
        return self.numero_factura

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, models.SET_NULL, db_column='id_categoria', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'producto'
    
    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    rut_proveedor = models.CharField(unique=True, max_length=13)
    nombre_proveedor = models.CharField(unique=True, max_length=200)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'
        
    def __str__(self):
        return self.nombre_proveedor


class TablaVistaFactura(models.Model):
    numero_factura = models.IntegerField(db_column='NUMERO_FACTURA')  # Field name made lowercase.
    fecha = models.CharField(db_column='FECHA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hora = models.CharField(db_column='HORA', max_length=13, blank=True, null=True)  # Field name made lowercase.
    rut_cliente = models.CharField(db_column='RUT_CLIENTE', max_length=15)  # Field name made lowercase.
    razon_social = models.CharField(db_column='RAZON_SOCIAL', max_length=100)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.CharField(db_column='SUBTOTAL', max_length=55, blank=True, null=True)  # Field name made lowercase.
    iva = models.CharField(db_column='IVA', max_length=54, blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='TOTAL', max_length=48, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tabla_vista_factura'
    
    def __str__(self):
        return self.numero_factura


class Venta(models.Model):
    ORIGENES = [('web', 'Web'), ('chatbot', 'Chatbot'), ('directo', 'Venta directa')]
    id_venta       = models.AutoField(primary_key=True)
    fecha          = models.DateTimeField()
    total          = models.IntegerField()
    tipo_documento = models.CharField(max_length=7)
    origen         = models.CharField(max_length=10, default='web', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'venta'

    def __str__(self):
        return str(self.fecha)


class ConversacionWhatsapp(models.Model):
    telefono  = models.CharField(max_length=30)
    rol       = models.CharField(max_length=10)   # 'user' | 'assistant'
    contenido = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversacion_whatsapp'
        ordering = ['fecha']

    def __str__(self):
        return f'{self.telefono} [{self.rol}] {self.fecha:%d/%m %H:%M}'


class ConversacionEstado(models.Model):
    ESTADOS = [
        ('en_consulta',        'En consulta'),
        ('interesado',         'Interesado'),
        ('cotizacion_enviada', 'Cotización enviada'),
        ('concretada',         'Compra concretada'),
        ('abandonada',         'Abandonó el carrito'),
    ]
    telefono   = models.CharField(max_length=30, unique=True)
    estado     = models.CharField(max_length=25, choices=ESTADOS, default='en_consulta')
    notas      = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversacion_estado'

    def __str__(self):
        return f'{self.telefono} → {self.estado}'


class Vendedor(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendedor'

    def __str__(self):
        return self.nombre


class VentaVendedor(models.Model):
    id_venta = models.OneToOneField(
        Venta, models.CASCADE,
        db_column='id_venta',
        related_name='info_vendedor',
    )
    id_vendedor = models.ForeignKey(
        Vendedor, models.SET_NULL,
        null=True, blank=True,
        db_column='id_vendedor',
        related_name='ventas',
    )
    id_cliente = models.IntegerField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=200, null=True, blank=True)
    neto = models.IntegerField(default=0)
    comision = models.IntegerField(default=0)

    class Meta:
        db_table = 'venta_vendedor'

    def __str__(self):
        return f'Venta {self.id_venta_id}'


class EtiquetaProducto(models.Model):
    producto = models.OneToOneField(
        Producto, on_delete=models.CASCADE,
        db_column='id_producto', related_name='etiqueta',
    )
    archivo_delantera = models.FileField(upload_to='etiquetas/', blank=True, null=True)
    archivo_especificaciones = models.FileField(upload_to='etiquetas/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'etiqueta_producto'

    def __str__(self):
        return f'Etiqueta {self.producto.nombre}'


class ConfiguracionEtiqueta(models.Model):
    TIPOS_PAPEL = [
        ('carta',        'Carta (216×279 mm)'),
        ('a4',           'A4 (210×297 mm)'),
        ('oficio',       'Oficio (216×330 mm)'),
        ('personalizado','Personalizado'),
    ]
    ORIENTACIONES = [
        ('portrait',  'Vertical'),
        ('landscape', 'Horizontal'),
    ]
    tipo_papel   = models.CharField(max_length=15, choices=TIPOS_PAPEL, default='carta')
    ancho_mm     = models.DecimalField(max_digits=7, decimal_places=2, default=216)
    alto_mm      = models.DecimalField(max_digits=7, decimal_places=2, default=279)
    orientacion  = models.CharField(max_length=10, choices=ORIENTACIONES, default='portrait')

    class Meta:
        db_table = 'configuracion_etiqueta'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
