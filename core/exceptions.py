# System Utils
from django.http import JsonResponse

# Installed Utils
from rest_framework.views import exception_handler
from rest_framework.response import Response  # Asegúrate de importar Response

def custom_exception_handler(exc, context):
    """
    Custom the exceptions
    messages
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
        
    if hasattr(exc, 'detail'):
        return JsonResponse(  # Cambiado de `response(...)` a `JsonResponse(...)`
            {
                "success": False,
                "message": exc.detail
            },
            status=response.status_code  # Asegúrate de incluir el código de estado
        )      
    else:
        return JsonResponse({
            'success': False,  # Corregido 'sucess' a 'success'
            'message': 'An unknown error occurred.'
        }, status=500)
