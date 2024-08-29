from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.Integer, nullable=False)
    services = db.relationship('Servico', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.username}>'

    def to_dict(self):
        return {"id": self.id, "fullname": self.fullname, "username": self.username, "email": self.email, "senha": self.senha, "foto": self.foto, "services": self.services}

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    # Foreign Key referencing Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    app_web = db.Column(db.Boolean, default=False)
    app_android = db.Column(db.Boolean, default=False)
    app_IOS = db.Column(db.Boolean, default=False)
    app_exe = db.Column(db.Boolean, default=False)
    app_complex = db.Column(db.Integer, nullable=True)
    obs = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<Servico {self.name}>'

    def to_dict(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "cliente_id": self.cliente_id,
            "app_web": self.app_web,
            "app_android": self.app_android,
            "app_IOS": self.app_IOS,
            "app_exe": self.app_exe,
            "app_complex": self.app_complex
        }
