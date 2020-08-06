from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta
from flask_cors import CORS



app = Flask(__name__)
app.config['SECRET_KEY'] = 'h4NqVcf7cUcTDEJkfcVijfd52LFeu7wSCEBbXJNv73WsfLrg2ThzGDhYaFEcEnC377k4hfhCxLFhx3WsufdvFCDcSQgUUDAXqzBnqRhjwrMbw7o9We7SsT2PFAcgzLyK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


db = SQLAlchemy(app)
CORS(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Please Login to continue"
login_manager.login_message_category = "info"


final_url = 'http://localhost:5000'


from app import routes
