from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from app import app

# Cria um Blueprint para o módulo 'default'
api = Blueprint('api', __name__)

# Decorador que verifica se o usuário está logado
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')#http://127.0.0.1:5000/route?token=
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': f'{e}'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

# Rota para a página inicial
@api.route('/service', methods=['GET', 'POST'])
@token_required
def index():
    token = request.args.get('token')
    return jsonify({'message': jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')})