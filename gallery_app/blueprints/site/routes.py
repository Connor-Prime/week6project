from flask import Blueprint, render_template, request, redirect, flash, session

from ...forms import ImageAlbumForm, ImageForm, UpdateAlbumForm, UpdateImageForm
from ...models import Album, db, User, login_manager, albums_schema, AlbumImage
from flask_login import current_user

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():

    if current_user != None:
        albums = Album.query.filter(Album.user_id==current_user.get_id())
    else:
        albums = None

    print(current_user.get_id())

    return render_template('home.html', albums = albums)



@site.route('/home/view_album/<id>')
def view_album(id):
    

    images = AlbumImage.query.filter(AlbumImage.album_id==id)

    return render_template('view_images.html',images=images, album_id =id)


@site.route('/create_album', methods=['GET','POST'])
def open():

    form = ImageAlbumForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        thumbnail = form.thumbnail.data

        user = current_user

        album =Album(user.get_id(),thumbnail, name)

        db.session.add(album)
        db.session.commit()
        

        flash(f"{name} has been added to your Photo Albums.")
        return redirect('/', )

    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/create_album')

    return render_template('create_album.html', form = form)

@site.route('/home/update_album/<id>', methods=['GET','POST'])
def update_album(id):

    form = UpdateAlbumForm()

    album = Album.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        album.name = form.name.data
        album.thumbnail = form.thumbnail.data


        db.session.commit()
        

        flash(f"{album.name} has been updated.")
        return redirect('/')
    


    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/create_album')

    return render_template('updatealbum.html', form = form)
    


@site.route('/home/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    album = Album.query.get(id)
    images = AlbumImage.query.filter(AlbumImage.album_id==id) 




    if current_user.get_id()== album.user_id:

        for image in images:
            db.session.delete(image)

        db.session.delete(album)
        db.session.commit()

    return redirect('/')

# Routes for updating images within a albumn

@site.route('/home/add_image/<id>', methods=['POST','GET'])
def create_image(id):

    form = ImageAlbumForm()

    album = Album.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        img = form.thumbnail.data
        img = AlbumImage(id, img, name=name)

        db.session.add(img)
        db.session.commit()
        

        flash(f"{name} has been added to your Photo Album.", category="success")
        return redirect(f'/home/view_album/{id}')

    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/home/add_image/<id>')

    return render_template('imagealbum.html', form = form, album=album)


@site.route('/home/update_image/<id>', methods=['GET','POST'])
def update_image(id):

    form = UpdateImageForm()

    img = AlbumImage.query.get(id)

    album_id = img.album_id

    

    if request.method == 'POST' and form.validate_on_submit():
        img.name = form.name.data
        img.img = form.thumbnail.data


        db.session.commit()
        

        flash(f"{img.name} has been updated.")
        return redirect(f'/home/view_album/{album_id}')

    


    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/home/update_image/{id}')

    return render_template('update_img.html', form = form)

@site.route('/home/delete_image/<id>')
def delete_image(id):

    #query our database to find that object we want to delete
    image = AlbumImage.query.get(id)

    album_id = image.album_id
    db.session.delete(image)
    db.session.commit()

    return redirect(f'/home/view_album/{album_id}')

