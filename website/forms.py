from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, NumberRange, Length
from flask_wtf.file import FileRequired, MultipleFileField, FileField


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    profile_photo = FileField('Profile Photo')
    submit = SubmitField('Upload')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6)])
    change_password = SubmitField('Change Password')

class ShopItemForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2)])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_images = MultipleFileField('Product Images',validators=[FileRequired()])  # multiple images
    hashtags = StringField('Hashtags')
    flash_sale = BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'),
                                                        ('Accepted', 'Accepted'),
                                                        ('Out of Stock', 'Out of Stock'),
                                                        ('Delivered', 'Delivered'),
                                                        ('Cancelled', 'Cancelled')])
    update = SubmitField('Update Status')