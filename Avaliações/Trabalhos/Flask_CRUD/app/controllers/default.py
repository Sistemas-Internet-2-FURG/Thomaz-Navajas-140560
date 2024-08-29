from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.tables import Cliente, Servico
import random as rd

# Cria um Blueprint para o módulo 'default'
default = Blueprint('default', __name__)

# Decorador que verifica se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Redireciona pra página inicial se o usuário não estiver logado
        if 'username' not in session:
            return redirect(url_for('default.index'))
        return f(*args, **kwargs)
    return decorated_function

# Rota para a página inicial
@default.route('/', methods=['GET', 'POST'])
def index():
    # Se o método da requisição for POST
    if request.method == 'POST':
        print(request.form) # Imprime os dados do formulário no console
        
        # Verifica se o email foi enviado
        if 'email' in request.form:
            fullname = request.form['fullname'] # Obtém o nome completo
            username = request.form['username'] # Obtém o nome de usuário
            email = request.form['email'] # Obtém o e-mail
            password = request.form['password'] # Obtém a senha
            foto = rd.randint(0,19) # Obtém a senha
            
            # Verifica se o nome de usuário já existe no banco de dados
            user = Cliente.query.filter_by(username=username).first()
            if user:
                error = ['register','Esse nome de usuário já existe. Por favor, escolha outro.']
                return render_template('index.html', error=error) # Retorna erro na tela de registro
            else:
                # Verifica se o email já está em uso
                user = Cliente.query.filter_by(email=email).first()
                if user:
                    error = ['register','Esse E-mail já está sendo utilizado. Por favor, escolha outro.']
                    return render_template('index.html', error=error) # Retorna erro na tela de registro
                else:
                    # Cria um novo usuário se não houver conflitos
                    hashed_password = generate_password_hash(password) # Criptografa a senha
                    new_user = Cliente(fullname=fullname, username=username, email=email, senha=hashed_password, foto=foto)
                    db.session.add(new_user) # Adiciona o novo usuário à sessão do banco de dados
                    db.session.commit() # Salva as alterações no banco de dados
                    user = Cliente.query.filter_by(username=new_user.username).first_or_404() # Busca o usuário pelo nome
                    session['user_id'] = user.id  # Armazena o ID do usuário na sessão pra segurança
                    session['username'] = user.username  # Armazena o nome de usuário na sessão pra conveniência
                    session['perfil_photo'] = foto
                    return redirect(url_for('default.user', username=username)) # Redireciona pra página do usuário

                    services = Servico.query.filter_by(cliente_id=user.id).all() # Busca todos os serviços do cliente
                    print(user)
                    # Exibe a página do usuário com os serviços
                    return render_template('user.html', user=session['username'], services=services, username=username)
        else:
            # Processo de login
            username = request.form['username'] # Obtém o nome de usuário
            password = request.form['password'] # Obtém a senha
            user = Cliente.query.filter_by(username=username).first() # Busca o usuário pelo nome de usuário

            # Verifica se a senha está correta
            if user and check_password_hash(user.senha, password): 
                session['user_id'] = user.id  # Armazena o ID do usuário na sessão
                session['username'] = user.username  # Armazena o nome de usuário na sessão
                session['perfil_photo'] = user.foto
                return redirect(url_for('default.user', username=username)) # Redireciona para a página do usuário
            else:
                error = ['login','Nome de usuário ou senha incorretos.'] # Mensagem de erro se login falhar
                return render_template('index.html', error=error) # Retorna erro na tela de login
    else: # Se o método for GET
        if 'username' not in session:
            return render_template('index.html') # Exibe a página de login
        else:
            return redirect(url_for('default.user', username=session['username'])) # Redireciona pra página do usuário logado

# Rota para logout
@default.route('/logout')
def logout():
    session.clear() # Limpa a sessão do usuário
    return redirect(url_for('default.index')) # Redireciona pra página inicial

# Rota para a página do usuário
@default.route('/user/<username>', methods=['GET', 'POST', 'PUT'])
@login_required# Garante que o usuário esteja logado
def user(username):
    if request.method == 'POST': # Se o método da requisição for POST
        if '_method' in request.form: # Verifica se o formulário de edição de serviço foi enviado
            if request.form['_method'] == 'PUT':
                if 'service_id' in request.form:
                    client_id = session['user_id'] # Obtém o ID do cliente da sessão
                    user = Cliente.query.filter_by(id=client_id).first_or_404() # Busca o usuário pelo id
                    service = Servico.query.filter_by(name=request.form['service_name']).first() # Busca se tem serviços com o mesmo nome
                    print(request.form['service_id'])
                    print(service.id)
                    if int(service.id) != int(request.form['service_id']): # verifica se o serviços com o mesmo nome pertence cliente de id diferente
                        services = Servico.query.filter_by(cliente_id=client_id).all()
                        return render_template('user.html', username=session['username'], services=services, error=f'Já existe uma aplicação com o nome {request.form['service_name']}')
                    else:
                        service = Servico.query.filter_by(cliente_id=user.id, id=request.form['service_id']).first_or_404()# Busca todos os serviços do cliente
                        service.name = request.form['service_name'] # Obtém o nome do serviço
                        # Verifica quais opções foram selecionadas no formulário
                        if 'app_web' in request.form:
                            service.app_web = True
                        else:
                            service.app_web = False
                        if 'app_android' in request.form:
                            service.app_android = True
                        else:
                            service.app_android = False
                        if 'app_IOS' in request.form:
                            service.app_IOS = True
                        else:
                            service.app_IOS = False
                        if 'app_exe' in request.form:
                            service.app_exe = True
                        else:
                            service.app_exe = False

                        service.app_complex = request.form['app_complex'] # Obtém a complexidade da aplicação
                        service.app_obs = request.form['app_obs'] # Obtém observações sobre a aplicação
                        db.session.commit()
                        services = Servico.query.filter_by(cliente_id=client_id).all()
                        return render_template('user.html', username=session['username'], services=services)
            elif request.form['_method'] == 'DELETE':
                Servico.query.filter_by(id=request.form['service_id']).delete()
                services = Servico.query.filter_by(cliente_id=session['user_id']).all()
                db.session.commit()
                return render_template('user.html', username=session['username'], services=services, error=f'Aplicação excluída com sucesso!')

        # Verifica se o nome do serviço foi enviado
        if 'service_name' in request.form:
            service_name = request.form['service_name'] # Obtém o nome do serviço
            service = Servico.query.filter_by(name=service_name).first()

            # Verifica se o serviço já existe
            if service:
                error = ['service_name','Você já possui um serviço com esse nome. Por favor, escolha outro.']
                return render_template('user.html', error=error) # Retorna erro se o serviço já existir
            else:
                client_id = session['user_id'] # Obtém o ID do cliente da sessão
                user = Cliente.query.filter_by(id=client_id).first()
                # Verifica quais opções foram selecionadas no formulário
                if 'app_web' in request.form:
                    app_web = True
                else:
                    app_web = False
                if 'app_android' in request.form:
                    app_android = True
                else:
                    app_android = False
                if 'app_IOS' in request.form:
                    app_IOS = True
                else:
                    app_IOS = False
                if 'app_exe' in request.form:
                    app_exe = True
                else:
                    app_exe = False

                app_complex = request.form['app_complex'] # Obtém a complexidade da aplicação
                app_obs = request.form['app_obs'] # Obtém observações sobre a aplicação

                # Cria um novo serviço
                new_service = Servico(name=service_name, status='Pendente', cliente_id=user.id, app_web=app_web, app_android=app_android, app_IOS=app_IOS, app_exe=app_exe, app_complex=app_complex, obs=app_obs)
                db.session.add(new_service)
                db.session.commit()
                services = Servico.query.filter_by(cliente_id=session['user_id']).all()
                return redirect(url_for('default.user', username=session['username'], services=services))
    else: # Se o método for GET
        user = Cliente.query.filter_by(username=username).first_or_404() # Busca o usuário pelo nome
        services = Servico.query.filter_by(cliente_id=user.id).all() # Busca todos os serviços do cliente
        print(user)

        # Exibe a página do usuário com os serviços
        return render_template('user.html', user=session['username'], services=services, username=username)

# Rota para adicionar um novo serviço
@default.route('/user/add_service', methods=['GET'])
@login_required # Garante que o usuário esteja logado
def add_service():
    return render_template('service_register.html')


# Delete
@default.route('/item/<int:id>', methods=['DELETE'])
@login_required # Garante que o usuário esteja logado
def delete_item(id):
    item = Cliente.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

"""
# CRUD Operations
# Create
@default.route('/clientes', methods=['POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name') 
        new_item = Cliente(name=name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    else:
        return jsonify({"error": "Invalid request method"}), 405

# Read
@default.route('/clientes', methods=['GET'])
def get_items():
    items = Cliente.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@default.route('/clientes/<int:id>', methods=['GET'])
def get_item(id):
    item = Cliente.query.get_or_404(id)
    return jsonify(item.to_dict()), 200

# Update
@default.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Cliente.query.get_or_404(id)
    item.name = data['name']
    db.session.commit()
    return jsonify(item.to_dict()), 200

# Delete
@default.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Cliente.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
"""