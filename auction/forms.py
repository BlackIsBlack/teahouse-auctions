
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, SelectField, DecimalField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
from .submitFields import getListContents

# Allowed file types for image uploading
ALLOWED_IMAGE_TYPES = {'png','jpg','jpeg','PNG','JPG','JPEG'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_num = StringField("Contact Number", validators=[InputRequired()])

    address = StringField('Address', validators=[InputRequired()])

    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    teaName = StringField('Ingredients', validators=[InputRequired()])
    country = SelectField('Country of Origin', choices=getListContents('countries'), validators=[InputRequired()])
    oxidation = SelectField('Oxidation', choices=getListContents('oxides'), validators=[InputRequired()])
    packingType = SelectField('Packing', choices=getListContents('packing'), validators=[InputRequired()])
    weight = DecimalField('Weight',places=3, validators=[InputRequired()])
    photos = FileField('Add Photos', validators=[FileRequired(message='An image must be selected.'), FileAllowed(ALLOWED_IMAGE_TYPES, message='Valid image types are png, jpg, jpeg, PNG, JPG, and JPEG')])
    description = TextAreaField('Description', validators=[InputRequired()])
    startBid = DecimalField('Starting Bid',places=3,validators=[InputRequired()])
    duration = IntegerField('Auction Duration (Hours)', validators=[InputRequired()])
    submit = SubmitField('Submit')
