from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, LoginHomeForm, RegistrationHomeForm, ItemForm
from app.models import User, Home, Item


@app.route('/test', methods=['GET', 'POST'])
def test():
    return  render_template('test.html')

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    items = current_user.get_items().all()
    print(items)

    form = LoginHomeForm()
    if form.validate_on_submit():
        home = Home.query.filter_by(home_name=form.home_name.data).first()
        if home is None or not home.check_password(form.password.data):
            flash('Invalid home name or password')
            return redirect(url_for('index'))
        current_user.home_id = home.id
        db.session.commit()
        flash('Congratulations, you are part of home!')

        return redirect(url_for('index'))
    form_item = ItemForm()
    if form_item.validate_on_submit():
        item = Item(item_name=form_item.item_name.data, type=form_item.type.data,
                    amount=form_item.amount.data, note=form_item.note.data,
                    bought=False, author_item=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item is now added!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', items=items, form=form, form_item=form_item)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/register_home', methods=['GET', 'POST'])
@login_required
def register_home():
    if current_user.home_id:
        return redirect(url_for('index'))
    form = RegistrationHomeForm()
    if form.validate_on_submit():
        home = Home(home_name=form.home_name.data)
        home.set_password(form.password.data)
        db.session.add(home)
        db.session.commit()
        flash('Congratulations, you created a new home!')
        return redirect(url_for('index'))
    return render_template('register_home.html', title='Register home', form=form)

@app.route('/change_home')
def change_home():
    current_user.home_id = 0
    db.session.commit()
    return redirect(url_for('index'))