from blog import create_app, db
from blog.admin import admin_bp, init_app
import os
app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://userimec:Pin.1234@172.16.1.13:5432/pyapp1"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')


init_app(app)

app.register_blueprint(admin_bp, url_prefix='/admin')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)