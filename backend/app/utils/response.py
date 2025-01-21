from flask import jsonify

def success_response(data, message, status_code):
    return jsonify({
        'data': data,
        'message': message
    }), status_code

def error_response(error, message, status_code):
    return jsonify({
        'error': error,
        'message': message
    }), status_code
