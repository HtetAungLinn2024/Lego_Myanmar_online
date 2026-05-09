from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_database(app):
    db.init_app(app)
    db.create_all()
    print('Database created.')


def create_app():

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config['SECRET_KEY'] = 'AIT'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/') #localhost5000/views
    app.register_blueprint(auth, url_prefix='/') #localhost5000/login
    app.register_blueprint(admin, url_prefix='/') #localhost5000/admin

    with app.app_context():
        create_database(app)

    return app