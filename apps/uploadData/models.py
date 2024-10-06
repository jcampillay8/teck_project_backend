from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Teck_Inventory_Balance_05(models.Model):
    Artículo = models.AutoField(primary_key=True)
    Descripción = models.CharField(max_length=255)
    Stock_total = models.IntegerField()
    Cantidad_reservada = models.IntegerField()
    Cantidad_disponible = models.IntegerField()
    Costo_promedio = models.DecimalField(max_digits=15, decimal_places=2)
    Last_PO_Vendor_Date = models.DateField()
    Last_PO_Vendor = models.CharField(max_length=255)
    Quantity_to_buy = models.IntegerField()

    def __str__(self):
        return str(self.Artículo)


class Teck_Inventory_Balance(models.Model):
    Artículo = models.AutoField(primary_key=True)
    Descripción = models.CharField(max_length=255)
    Stock_total = models.CharField(max_length=255)
    Cantidad_reservada = models.CharField(max_length=255)
    Cantidad_disponible = models.CharField(max_length=255)
    Costo_promedio = models.CharField(max_length=255)
    Last_PO_Number = models.CharField(max_length=255)
    Last_PO_Vendor_Date = models.CharField(max_length=255)
    Last_PO_Vendor = models.CharField(max_length=255)
    Quantity_to_buy = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Artículo)


class DataFromCreatedTable(models.Model):
    # Campos para almacenar el archivo subido y la tabla creada
    file_name = models.CharField(max_length=255)           # Nombre del archivo subido
    file_sheet = models.CharField(max_length=255)          # Nombre de la hoja (solo para archivos Excel)
    start_cell = models.CharField(max_length=5)            # Celda de inicio donde comienza la tabla
    name_table = models.CharField(max_length=255)          # Nombre de referencia de la tabla creada

    # Relación genérica para asociar la tabla creada
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_table = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.file_name} - {self.name_table}"

class Teck_Inventory_Balance_02(models.Model):
    Artículo = models.AutoField(primary_key=True)
    Descripción = models.CharField(max_length=255)
    Stock_total = models.CharField(max_length=255)
    Cantidad_reservada = models.CharField(max_length=255)
    Cantidad_disponible = models.CharField(max_length=255)
    Costo_promedio = models.CharField(max_length=255)
    Last_PO_Vendor = models.CharField(max_length=255)
    Last_PO_Number = models.CharField(max_length=255)
    Last_PO_Vendor_Date = models.CharField(max_length=255)
    Quantity_to_buy = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Artículo)
