# backend/apps/uploadData/views.py
import os
import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.db import models
from django.conf import settings
from django.core.management import call_command
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UploadFileView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        # Cargar archivo desde el formulario
        file = request.data.get('file')
        sheet_name = request.data.get('sheet_name', None)
        start_location = request.data.get('start_location', 'A1')

        if not file:
            return Response({"error": "No se proporcionó un archivo."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if file.name.endswith('.xls'):
                # Procesar archivo .xls
                df = pd.read_excel(file, sheet_name=sheet_name, engine='xlrd')
            elif file.name.endswith('.xlsx'):
                # Procesar archivo .xlsx
                df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
            else:
                return Response({"error": "Tipo de archivo no soportado."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si la tabla comienza en A1 o en otra celda
            if start_location.lower() != 'a1':
                # Convertir la celda de inicio a índices de fila y columna
                start_cell = start_location.upper()
                start_row = int(start_cell[1:]) - 1  # Restar 1 porque pandas usa índice 0
                start_col_letter = ''.join([c for c in start_cell if c.isalpha()])  # La letra de la columna
                start_col = ord(start_col_letter) - ord('A')  # Convertir letra de columna a índice numérico

                # Leer el archivo completo sin asumir encabezado
                df = pd.read_excel(file, sheet_name=sheet_name, header=None)

                # Filtrar las filas y columnas desde la celda especificada
                df = df.iloc[start_row:, start_col:]

                # Ajustar el header a partir de la primera fila de datos de la selección
                df.columns = df.iloc[0]
                df = df[1:]

            # Manejar valores NaN reemplazándolos por una cadena vacía
            df.columns = df.columns.fillna('')
            df = df.fillna('')

            # Devolver los encabezados para la selección
            headers = list(df.columns)
            return Response({"headers": headers}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# backend/apps/uploadData/views.py
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command
from django.apps import apps
from django.db import models
from apps.uploadData.models import DataFromCreatedTable  # Importa tu modelo DataFromCreatedTable

class CreateTableView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        selected_columns = request.data.get('selected_columns', [])
        table_name = request.data.get('table_name', 'DynamicTable')
        file_name = request.data.get('file_name', 'Unknown_File')
        file_sheet = request.data.get('file_sheet', 'Unknown_Sheet')
        start_location = request.data.get('start_location', 'A1')

        if not selected_columns:
            return Response({"error": "No se seleccionaron columnas."}, status=status.HTTP_400_BAD_REQUEST)

        # Definir dinámicamente un modelo para la nueva tabla
        fields = {}
        for column in selected_columns:
            column_name = column["name"].replace(" ", "_")
            column_type = column["type"]

            # Ajustar el tipo de datos según el valor de la columna
            if column_type == "Id":
                fields[column_name] = models.AutoField(primary_key=True)
            elif column_type == "Texto Corto":
                fields[column_name] = models.CharField(max_length=255)
            elif column_type == "Texto Largo":
                fields[column_name] = models.TextField()
            elif column_type == "Número Entero":
                fields[column_name] = models.IntegerField()
            elif column_type == "Número con Decimal":
                fields[column_name] = models.DecimalField(max_digits=15, decimal_places=2)
            elif column_type.startswith("Fecha"):
                fields[column_name] = models.DateField()
            elif column_type == "Booleano":
                fields[column_name] = models.BooleanField()
            elif column_type == "Lista":
                fields[column_name] = models.JSONField()
            elif column_type in ["Moneda Peso Chileno ($)", "Moneda Dólar USA (US$)"]:
                fields[column_name] = models.DecimalField(max_digits=15, decimal_places=2)
            else:
                fields[column_name] = models.CharField(max_length=255)

        # Crear un modelo dinámico
        try:
            NewModel = type(table_name, (models.Model,), {**fields, '__module__': 'apps.uploadData.models'})
        except Exception as e:
            return Response({"error": f"Error al crear el modelo dinámico: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Registrar dinámicamente el modelo
        try:
            apps.register_model('uploadData', NewModel)
        except Exception as e:
            return Response({"error": f"Error al registrar el modelo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Actualizar el archivo models.py y admin.py
        try:
            models_file_path = 'apps/uploadData/models.py'
            admin_file_path = 'apps/uploadData/admin.py'
            with open(models_file_path, 'r') as f:
                content = f.read()

            # Verificar si el import ya existe
            if "from django.db import models" not in content:
                content = "from django.db import models\n\n" + content

            # Definir el nuevo modelo en formato de texto
            new_model_code = f"""
class {table_name}(models.Model):\n"""
            for column in selected_columns:
                column_name = column["name"].replace(" ", "_")
                column_type = column["type"]
                field_line = f"    {column_name} = "

                if column_type == "Id":
                    field_line += "models.AutoField(primary_key=True)\n"
                elif column_type == "Texto Corto":
                    field_line += "models.CharField(max_length=255)\n"
                elif column_type == "Texto Largo":
                    field_line += "models.TextField()\n"
                elif column_type == "Número Entero":
                    field_line += "models.IntegerField()\n"
                elif column_type == "Número con Decimal":
                    field_line += "models.DecimalField(max_digits=15, decimal_places=2)\n"
                elif column_type.startswith("Fecha"):
                    field_line += "models.DateField()\n"
                elif column_type == "Booleano":
                    field_line += "models.BooleanField()\n"
                elif column_type == "Lista":
                    field_line += "models.JSONField()\n"
                elif column_type in ["Moneda Peso Chileno ($)", "Moneda Dólar USA (US$)"]:
                    field_line += "models.DecimalField(max_digits=15, decimal_places=2)\n"
                else:
                    field_line += "models.CharField(max_length=255)\n"

                new_model_code += field_line

            # Agregar el método __str__
            new_model_code += f"\n    def __str__(self):\n        return str(self.{selected_columns[0]['name'].replace(' ', '_')})\n"

            # Agregar el nuevo modelo al contenido del archivo
            content += f"\n{new_model_code}"

            # Sobrescribir el archivo models.py
            with open(models_file_path, 'w') as f:
                f.write(content)

            # Actualizar el archivo admin.py
            with open(admin_file_path, 'r') as f:
                admin_content = f.read()

            # Verificar si el import ya existe
            if "from django.contrib import admin" not in admin_content:
                admin_content = "from django.contrib import admin\n\n" + admin_content

            # Buscar si ya existe una línea con `from .models import`
            if "from .models import" in admin_content:
                start_index = admin_content.index("from .models import") + len("from .models import")
                existing_imports = admin_content[start_index:].splitlines()[0].strip()
                updated_imports = f"{existing_imports}, {table_name}"
                admin_content = admin_content.replace(f"from .models import {existing_imports}", f"from .models import {updated_imports}")
            else:
                # Si no existe, agregar una nueva línea de importación
                admin_content += f"from .models import {table_name}\n"

            # Agregar una clase personalizada para mostrar todas las columnas en Django Admin
            list_display = ", ".join([f"'{column['name'].replace(' ', '_')}'" for column in selected_columns])
            admin_class_code = f"""
@admin.register({table_name})
class {table_name}Admin(admin.ModelAdmin):
    list_display = ({list_display})
"""

            admin_content += admin_class_code

            # Sobrescribir el archivo admin.py
            with open(admin_file_path, 'w') as f:
                f.write(admin_content)

        except Exception as e:
            return Response({"error": f"Error al actualizar el archivo models.py o admin.py: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Aplicar migración para crear la tabla
        try:
            call_command('makemigrations', 'uploadData')
            call_command('migrate', 'uploadData')
        except Exception as e:
            return Response({"error": f"Error al aplicar migraciones: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Crear un registro en DataFromCreatedTable
        try:
            content_type = ContentType.objects.get_for_model(NewModel)
            DataFromCreatedTable.objects.create(
                content_type=content_type,
                object_id=0,  # `object_id` no se usa ya que no estamos referenciando una instancia específica
                file_name=file_name,
                file_sheet=file_sheet,
                start_cell=start_location,
                name_table=table_name,
            )
        except Exception as e:
            return Response({"error": f"Error al crear el registro en DataFromCreatedTable: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": f"Tabla '{table_name}' creada exitosamente en la base de datos."}, status=status.HTTP_201_CREATED)
