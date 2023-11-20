from werkzeug.security import generate_password_hash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object


class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(30),unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.user_id = self.set_id()
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def get_id(self):
            return str(self.user_id)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    
# Albums contain images and a thumbnail and are user specific.
class Album(db.Model):
    album_id = db.Column(db.String, primary_key = True, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    name = db.Column(db.String(50))
    album_image = db.relationship('AlbumImage', backref='Album',lazy=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable = False)

    def __init__(self, user_id, thumbnail, name):
        self.album_id = self.set_id()
        self.thumbnail = thumbnail
        self.user_id = user_id
        self.name = name


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self,img):
        self.image =img
        return self.image
    
    def __repr__(self):
        return f"<Album: {self.name}>"
    
class AlbumImage(db.Model):
    image_id = db.Column(db.String, primary_key = True, nullable=False)
    album_id = db.Column(db.String, db.ForeignKey('album.album_id'), nullable = False)

    img = db.Column(db.String, nullable=False)
    name = db.Column(db.String(50))

    def __init__(self, album_id, img, name):
        self.image_id = self.set_id()
        self.album_id = album_id
        self.img = img
        self.name = name

    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self,img):
        self.image =img
        return self.image
    

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ['album_id', 'name', 'thumbnail', 'user_id']


albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()