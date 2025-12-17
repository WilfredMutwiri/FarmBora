from rest_framework.response import Response


def handle_success(data=None, message="", status_code=200):
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return Response(response, status=status_code)

def handle_error(errors=None, message="", status_code=400):
    response = {
        "status": "error",
        "message": message,
        "errors": errors
    }
    return Response(response, status=status_code)

def handle_validation_error(errors=None, message="Validation Error", status_code=422):
    response = {
        "status": "fail",
        "message": message,
        "errors": errors
    }
    return Response(response, status=status_code)

def handle_not_found(message="Resource Not Found", status_code=404):
    response = {
        "status": "error",
        "message": message
    }
    return Response(response, status=status_code)

def handle_permission_denied(message="Permission Denied", status_code=403):
    response = {
        "status": "error",
        "message": message
    }
    return Response(response, status=status_code)