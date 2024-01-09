from extensions import database, app
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey, Column, String, Integer, Text, Interval
from sqlalchemy.orm import relationship
from extensions import login_manager

bcrypt = Bcrypt(app)


class User(database.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    role = Column(String, nullable=False)

    roles = ['admin', 'user']
    recipes = relationship('Recipe', backref='user')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Recipe(database.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    file = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    cooking_time = Column(Text, nullable=True)
    calories = Column(Integer, nullable=True)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = database.Column(Integer, ForeignKey('category.id'), nullable=False)

class Category(database.Model):
    id = database.Column(Integer, primary_key=True)
    name = database.Column(String(50), unique=True, nullable=False)
    recipes = database.relationship('Recipe', backref='category')


categories = ['main course', 'desserts', 'appetizers', 'holiday specials']


if __name__ == "__main__":
    with app.app_context():
        database.create_all()

        for category_name in categories:
            new_category = Category(name=category_name)
            database.session.add(new_category)
            database.session.commit()
