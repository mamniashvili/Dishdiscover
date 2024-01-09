from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User


class Signupform(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=4, max=12)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()

        if existing_user:
            raise ValidationError("This username is already in use. Please try another one.")

    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')


class Loginform(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username is not registered.')

    def validate_password(self, password):
        if self.username.data:
            user = User.query.filter_by(username=self.username.data).first()
            if user and not user.check_password(password.data):
                raise ValidationError('Incorrect password. Please try again.')


class Recipeform(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], )
    file = FileField('Image file', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    cooking_time = IntegerField('Cooking Time (minutes)')
    calories = IntegerField('Calories')
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    Category = SelectField('Category', validators=[DataRequired()],
                           choices=[(1, 'main course'), (2, 'desserts'), (3, 'appetizers'), (4, 'holiday specials')])

    submit = SubmitField('Submit Recipe')


class Editrecipeform(Recipeform):
    pass
