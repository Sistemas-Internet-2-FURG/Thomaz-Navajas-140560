from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '9nu%-QtE#15p$C9_w;!?U2I4ArtH7<(1*p8A[!#3#%wP+'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.controllers.default import default

app.register_blueprint(default)

from app.models.tables import Cliente  # Import your mode

with app.app_context():
    db.create_all()
        