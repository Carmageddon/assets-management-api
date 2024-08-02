from flask import request, jsonify
from functools import wraps
from marshmallow import ValidationError

def validate_payload(schema, many=False):
    """Validate payload schema for incoming requests"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                payload = schema(many=many).load(request.get_json(), unknown="exclude")
                kwargs["payload"] = payload
            except ValidationError as err:
                return jsonify({
                    "status": "error",
                    "message": "Information you've provided is not valid. Please update your input and try again.",
                    "errors": err.messages,
                }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
