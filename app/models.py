from app import db, login_manager, app
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(120), nullable=False)
    orders = db.relationship('TestOrder', backref='user')

    def __repr__(self):
        return f"User( '{self.id}', '{self.email}', '{self.phone}')"


class TestOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    no_of_test = db.Column(db.Integer)
    type_of_test = db.Column(db.String(40))
    appointment = db.Column(db.String(60), unique=False, nullable=True)
    address = db.Column(db.String(200), unique=False, nullable=True)
    landmark = db.Column(db.String(100), unique=False, nullable=True)
    payment_txn = db.Column(db.Integer, unique=False, nullable=True)
    status_txn = db.Column(db.String(40))
    report_status = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"TestOrder( '{self.id}','{self.name}','{self.no_of_test}', '{self.type_of_test}'," \
               f"'{self.appointment}','{self.address}','{self.landmark}'" \
               f",'{self.payment_txn}','{self.status_txn}','{self.report_status}','{self.user_id}')"


class Myadmin(AdminIndexView):
    def is_accessible(self):
        if current_user.email == 'varshithvmv@gmail.com':
            return True
        else:
            return False


from flask_admin.form.rules import Field


class CustomizableField(Field):
    def __init__(self, field_name, render_field='lib.render_field', field_args={}):
        super(CustomizableField, self).__init__(field_name, render_field)
        self.extra_field_args = field_args

    def __call__(self, form, form_opts=None, field_args={}):
        field_args.update(self.extra_field_args)
        return super(CustomizableField, self).__call__(form, form_opts, field_args)


class UserView(ModelView):
    column_list = (
        'id', 'name', 'user.phone', 'user.email', 'no_of_test', 'type_of_test', 'appointment', 'address', 'landmark',
        "payment_txn",
        'status_txn', 'report_status')
    column_searchable_list = (User.phone, User.email, TestOrder.payment_txn, TestOrder.name)
    can_export = True
    can_delete = False

    form_edit_rules = [
        CustomizableField('payment_txn', field_args={
            'readonly': True
        }),
        CustomizableField('report_status', field_args={
            'readonly': False
        }),
        # ... place other rules here
    ]
    can_edit = True


admin = Admin(app, index_view=Myadmin())

admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(TestOrder, db.session))
