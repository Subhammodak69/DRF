from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Global DRF exception handler.
    Normalises ALL error responses to:
        { "error": "<human-readable message>" }
    so the frontend always reads one key.
    """
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        # DRF wraps field/non-field errors in dicts/lists — flatten them
        if isinstance(data, dict):
            # Grab non_field_errors first (serializer-level errors)
            if 'non_field_errors' in data:
                messages = data['non_field_errors']
                message = messages[0] if messages else 'Validation error.'
            elif 'detail' in data:
                message = str(data['detail'])
            else:
                # Take first field error
                first_key = next(iter(data))
                val = data[first_key]
                if isinstance(val, list):
                    message = f"{first_key.replace('_', ' ').capitalize()}: {val[0]}"
                else:
                    message = str(val)
        elif isinstance(data, list):
            message = str(data[0]) if data else 'An error occurred.'
        else:
            message = str(data)

        response.data = {'error': str(message)}

    return response
