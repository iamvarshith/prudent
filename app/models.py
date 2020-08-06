from app import db, login_manager, app
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(120), unique=False, nullable=True)
    landmark = db.Column(db.String(60), unique=False, nullable=True)
    Time_date = db.Column(db.String(60), unique=False, nullable=True)
    type_of_test = db.Column(db.String(40))
    payment_txn = db.Column(db.Integer, unique=False, nullable=True)
    status = db.Column(db.String(40))
    no_of_patients = db.Column(db.Integer)

    def __repr__(self):
        return f"User( '{self.id}','{self.name}', '{self.email}','{self.address}','{self.landmark}','{self.Time_date}'" \
               f",'{self.payment_txn}','{self.patients}')"


class Myadmin(AdminIndexView):
    def is_accessible(self):
        if current_user.email == 'varshithvmv@gmail.com':
            return True
        else:
            return False


admin = Admin(app, index_view=Myadmin())

admin.add_view(ModelView(User, db.session))
