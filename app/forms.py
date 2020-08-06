from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateTimeField, \
    TextAreaField, FileField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, regexp, NumberRange
from flask import session


class RegistrationForm(FlaskForm):
    name = StringField('Username',
                       validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = IntegerField('Phone',
                         validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class PatientDetailsForm(FlaskForm):
    name = StringField('Username',
                       validators=[DataRequired(), Length(min=2, max=40)])

    address = TextAreaField('Username',
                          validators=[DataRequired(), Length(min=2, max=40)])
    landmark = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=40)])
    test_type = SelectField(u'Test Type', choices=[('RT-PCR', 'RT-PCR (price - 4000 &#8377;)'), ('Anti-DARS(antibody)',
                                            'Anti-DARS(antibody) (price - 1200 &#8377;) '), ('COV-2 IGG', 'COV-2 IGG (price - 1600 &#8377;) ')])
    no_of_patients = SelectField(u'Test Type',
                                 choices=[('1', 'one'), ('2', 'two'), ('3', 'three'), ('4', 'four'), ('5', 'five'),
                                          ('6', 'six'), ('7', 'seven'), ('8', 'eight')])
    date_time = StringField('Date and time of appointment')

    submit = SubmitField('Sign Up')


class Otp(FlaskForm):
    otp = IntegerField('OTP', validators=[DataRequired()])
    submit = SubmitField('Sign Up')



