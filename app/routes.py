from app import app, db
from app.models import User, Vocabular, Post
from app.forms import LoginForm, RegistrationForm, VokaPracticeForm,\
    VokaAddForm, EditProfileForm, PostForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import random

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

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
        user = User(username=form.username.data, email=form.email.data, len_level=form.level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/vocabulary_practice', methods=['GET', 'POST'])
@login_required
def voca_pract():
    translation = current_user.translations.order_by(Vocabular.last_check).first()
    g_set = ["Nice", "Exactly", "Good job", "Correct"]
    form = VokaPracticeForm()
    if form.validate_on_submit():
        translation.last_check = datetime.utcnow()
        db.session.commit()
        flash(g_set[random.randint(0, 3)])
        return redirect(url_for('voca_pract'))
    return render_template('voca_pract.html', title="Practice", form=form, translation=translation)

@app.route('/vocabulary_add', methods=['GET', 'POST'])
@login_required
def voca_add():
    form = VokaAddForm()
    if form.validate_on_submit():
        v = Vocabular(text=form.text.data, translate=form.translation.data,
                      owner=current_user)
        db.session.add(v)
        db.session.commit()
        flash('One more word added')
        return redirect(url_for('voca_add'))
    count = len(current_user.translations.all())
    #translations = current_user.translations.all()
    page = request.args.get('page', 1, type=int)
    translations = current_user.translations.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('voca_add', page=translations.next_num) \
        if translations.has_next else None
    prev_url = url_for('voca_add', page=translations.prev_num) \
        if translations.has_prev else None
    return render_template('voca_add.html', title="Add", form=form, translations=translations.items,
                           next_url=next_url, prev_url=prev_url, count=count)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/del_word/<word_id>')
@login_required
def del_word(word_id):
    v = Vocabular.query.get(word_id)
    db.session.delete(v)
    db.session.commit()
    return redirect(url_for('voca_add'))

@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('blog'))
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("blog.html", title='blog', form=form,
                           posts=posts.items, next_url=next_url, prev_url=prev_url)