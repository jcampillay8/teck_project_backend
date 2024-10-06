from django.contrib import admin

from .models import Teck_Inventory_Balance_05, Teck_Inventory_Balance, Teck_Inventory_Balance_02

@admin.register(Teck_Inventory_Balance_05)
class Teck_Inventory_Balance_05Admin(admin.ModelAdmin):
    list_display = ('Artículo', 'Descripción', 'Stock_total', 'Cantidad_reservada', 'Cantidad_disponible', 'Costo_promedio', 'Last_PO_Vendor_Date', 'Last_PO_Vendor', 'Quantity_to_buy')

@admin.register(Teck_Inventory_Balance)
class Teck_Inventory_BalanceAdmin(admin.ModelAdmin):
    list_display = ('Artículo', 'Descripción', 'Stock_total', 'Cantidad_reservada', 'Cantidad_disponible', 'Costo_promedio', 'Last_PO_Number', 'Last_PO_Vendor_Date', 'Last_PO_Vendor', 'Quantity_to_buy')

@admin.register(Teck_Inventory_Balance_02)
class Teck_Inventory_Balance_02Admin(admin.ModelAdmin):
    list_display = ('Artículo', 'Descripción', 'Stock_total', 'Cantidad_reservada', 'Cantidad_disponible', 'Costo_promedio', 'Last_PO_Vendor', 'Last_PO_Number', 'Last_PO_Vendor_Date', 'Quantity_to_buy')
