from flask_bcrypt import Bcrypt
from flask import render_template, flash, redirect, url_for
from forms import Signupform, Loginform, Recipeform, Editrecipeform
from extensions import *
from models import User, Recipe, Category
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os

bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if form.username.data.lower() == 'mari':
            user.role = 'admin'
        else:
            user.role = 'user'
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("successfully logged in!", "success")
                return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = Signupform()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)

        if form.username.data.lower() == 'mari':
            new_user.role = 'admin'
        else:
            new_user.role = 'user'

        database.session.add(new_user)
        database.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("successfully logged out!", "success")
    return redirect(url_for('home'))


categories = ['main course', 'desserts', 'appetizers', 'holiday specials']


@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    form = Recipeform()

    if form.validate_on_submit():
        file = form.file.data

        if file:
            filename = secure_filename(form.file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_recipe = Recipe(
                title=form.title.data,
                file=filename,
                description=form.description.data,
                cooking_time=form.cooking_time.data,
                calories=form.calories.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                user_id=current_user.id,
                category_id=form.Category.data
            )
            database.session.add(new_recipe)
            database.session.commit()
            return redirect(url_for('profile'))
        else:
            flash('No file provided for upload', 'error')
            return redirect(url_for('submit_recipe'))
    return render_template('submit_recipe.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", user=current_user, user_recipes=user_recipes)


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        return render_template('recipe.html', recipe=recipe)


@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if current_user.role == 'admin' or recipe.user_id == current_user.id:
        form = Editrecipeform(obj=recipe)

    if form.validate_on_submit():
        file = form.file.data

        if file:
            filename = secure_filename(form.file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            recipe.file = filename

        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.cooking_time = form.cooking_time.data
        recipe.calories = form.calories.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data

        database.session.commit()

        return redirect(url_for('profile'))

    return render_template("edit_recipe.html", form=form, recipe=recipe)


@app.route('/delete_recipe/<int:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if current_user.role == 'admin' or recipe.user_id == current_user.id:
        database.session.delete(recipe)
        database.session.commit()
        flash("Recipe deleted successfully", "success")

    return redirect(url_for('profile'))


@app.route('/holiday_specials')
def holiday_specials():
    category_name = 'holiday specials'
    category = Category.query.filter_by(name=category_name).first()

    if category:
        recipes = Recipe.query.filter_by(category=category).all()
        return render_template('holiday_specials.html', recipes=recipes)


@app.route('/main_course')
def main_course():
    category_name = 'main course'
    category = Category.query.filter_by(name=category_name).first()

    if category:
        recipes = Recipe.query.filter_by(category=category).all()
        return render_template('Main_course.html', recipes=recipes)


@app.route('/desserts')
def desserts():
    category_name = 'desserts'
    category = Category.query.filter_by(name=category_name).first()

    if category:
        recipes = Recipe.query.filter_by(category=category).all()
        return render_template('desserts.html', recipes=recipes)


@app.route('/appetizers')
def appetizers():
    category_name = 'appetizers'
    category = Category.query.filter_by(name=category_name).first()

    if category:
        recipes = Recipe.query.filter_by(category=category).all()
        return render_template('appetizers.html', recipes=recipes)
