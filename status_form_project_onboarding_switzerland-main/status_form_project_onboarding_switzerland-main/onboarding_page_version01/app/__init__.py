from flask import Flask
from app.routes import bp as main_bp

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # registro blueprints, caso necessário rotas diferentes de trabalho
    app.register_blueprint(main_bp)
    
    return app