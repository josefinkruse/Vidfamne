import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PictureForm, CommentForm, FolderForm
from flaskblog.models import User, Picture, Comment, Folder
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from datetime import date


@app.route("/")
@app.route("/all_pictures")
@login_required
def all_pictures():
    searchword= request.args.get('key', '')
    print(searchword)
    if searchword is not '':
        pictures = Picture.query\
            .filter(or_(Picture.description.contains(searchword), Picture.place_taken.contains(searchword))) \
            .order_by(Picture.id.desc()).all()
        return render_template('all_pictures.html', pictures=pictures, title='All pictures', searchword=searchword)
    else:
        print('\n\n', 'key not found', '\n\n')
        pictures = Picture.query.order_by(Picture.id.desc()).all()
        return render_template('all_pictures.html', pictures=pictures, title='All pictures')


@app.route("/my_pictures")
@login_required
def my_pictures():
    pictures = Picture.query.filter_by(user_id=current_user.id).order_by(Picture.id.desc()).all()
    return render_template('my_pictures.html', pictures=pictures, title='My pictures')


#   Ändra så vi vill ha den
@app.route("/start")
def start():
    return render_template('start.html', title='Start')


@app.route("/folders")
@login_required
def folders():
    folders_all = Folder.query.all()
    pictures = Picture.query.all()   # Do we need this??
    return render_template('folders.html', folders=folders_all, pictures=pictures, title='Albums')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_pictures'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_pictures'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('all_pictures'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Log out, Do we want to "confirm logout"?
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('start'))


# priofile pic?
def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Show and edit the users account
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title='Account',
                           profile_pic=profile_pic, form=form)


@app.route("/folder/new", methods=['GET', 'POST'])
@login_required
def new_folder():
    form = FolderForm()
    if form.validate_on_submit():
        folder = Folder(title=form.title.data,
                        start_date=(form.start_date.data),
                        end_date=(form.end_date.data),
                        destinations=form.destinations.data,
                        description=form.description.data)
        db.session.add(folder)
        db.session.commit()
        os.mkdir(f"flaskblog/static/trip_{folder.id}")
        picture_file = save_picture(form.folder_image.data, folder)
        folder.folder_image = picture_file
        db.session.commit()
        flash('Your folder has been created!', 'success')
        return redirect(url_for('folders'))
    return render_template('create_folder.html', title='Add Folder', form=form, legend='New Folder')


# Inside a folder?
@app.route("/folder/<int:folder_id>", methods=['GET', 'POST'])
@login_required
def folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    pictures = Picture.query.filter_by(folder_id=folder.id).order_by(Picture.id.desc()).all()
    return render_template('folder.html', title=folder.title, folder=folder, pictures=pictures)


def save_picture(form_image_file, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image_file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', f'trip_{folder.id}', picture_fn)

    i = Image.open(form_image_file)
    i.save(picture_path)

    return picture_fn

# Upload a new picture
# Originally: "/picture/new"  ?
@app.route("/folder/<int:folder_id>/picture/new", methods=['GET', 'POST'])
@login_required
def new_picture(folder_id):
    folder = Folder.query.get_or_404(folder_id)  # ???
    form = PictureForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.image_file.data, folder)
        picture = Picture(image_file=picture_file, date_taken=form.date_taken.data, place_taken=form.place_taken.data,
                          description=form.description.data, user=current_user, folder_id=folder.id) #...id(folder?) )
        db.session.add(picture)
        db.session.commit()
        flash(f'Your picture has been uploaded to album: {folder.title}!', 'success')
        return redirect(url_for('folder', folder_id=folder_id))
    return render_template('create_picture.html', title='Upload Picture', form=form, legend='New Picture')


# Comment a picture
@app.route("/picture/<int:picture_id>", methods=['GET', 'POST'])
@login_required
def picture(picture_id):         # , folder_id)???
    picture = Picture.query.get_or_404(picture_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated: # you can only comment if you're logged in
            comment = Comment(content=form.content.data, user=current_user, picture=picture)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been created!', 'success')
            return redirect(f'/picture/{picture.id}')
        else:
            flash('You are not logged in. You need to be logged in to be able to comment!', 'danger')
    # loading comments in the reverse order of insertion
    comments = Comment.query.filter_by(picture_id=picture_id).order_by(Comment.date_posted.desc()).all()
    return render_template('picture.html', title=f'picture-{picture.image_file}', picture=picture, form=form, comments=comments)


# Update a picture
@app.route("/picture/<int:picture_id>/update", methods=['GET', 'POST'])
@login_required
def update_picture(picture_id):
    picture = Picture.query.get_or_404(picture_id)
    if picture.author != current_user:
        abort(403)
    form = PictureForm()
    if form.validate_on_submit():
        picture.date_taken = form.date_taken.data
        picture.place_taken = form.place_taken.data
        picture.description = form.description.data
        db.session.commit()
        flash('Your picture has been updated!', 'success')
        return redirect(url_for('picture', picture_id=picture.id))
    elif request.method == 'GET':
        form.date_taken.data = picture.date_taken
        form.place_taken.data = picture.place_taken
        form.description.data = picture.description
    return render_template('edit_picture.html', title='Edit Picture',
                           form=form, legend='Edit Picture')


# Delete a picture
@app.route("/picture/<int:picture_id>/delete", methods=['POST'])
@login_required
def delete_picture(picture_id):
    folder_id = request.args.get("folder_id", None)
    picture = Picture.query.get_or_404(picture_id)
    if picture.author != current_user:
        abort(403)
    db.session.delete(picture)
    # Cant remove pictures with comments. Check if picture has comment, remove them first, and then remove picture
    db.session.commit()
    flash('Your picture has been deleted!', 'success')
    return redirect(url_for('folder', folder_id=folder_id))
