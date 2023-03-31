from functools import wraps

from flask import render_template, redirect, url_for, request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint

from blog import bcrypt
from blog.models import db, User2, Post2,Incident

from flask_admin import expose
from flask import Flask



admin_bp = Blueprint('admin_bp', __name__)





def init_app(app):


    admin = Admin(name=app.config.get('ADMIN_NAME', 'My App Admin'),
                  template_mode=app.config.get('ADMIN_TEMPLATE_MODE', 'bootstrap4'))
    admin.init_app(app)
    admin.add_view(ModelView(User2, db.session))
    admin.add_view(ModelView(Post2, db.session))




    class MyCustomView(ModelView):
            can_create = False
            can_edit = False
            can_delete = False
            column_list = ('id', 'location', 'description', 'phone_number', 'full_name', 'email', 'is_foundation_employee', 'dep', 'status', 'photo')

            def get_incidents(self):
                return db.session.query(Incident).all()

            @expose('/')
            def index(self):
                incidents = self.get_incidents()
                return self.render('incidents2.html', incidents=incidents)

    admin.add_view(MyCustomView(Incident, db.session))
    # Return None instead of admin
    return None


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return decorated_view


@admin_bp.route('/')
@login_required
def admin_panel():
    return render_template('admin')




