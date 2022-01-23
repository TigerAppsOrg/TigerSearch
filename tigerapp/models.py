# ----------------------------------------------------------------------
# models.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------
from tigerapp import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from tigerapp.config import DAYS_UNTIL_EXPIRE, DEFAULT_IMAGE, ADMIN_NETID
# ----------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

item_tags = db.Table("item_tags", db.Column('item_id', db.Integer,
        db.ForeignKey('items.id'), primary_key=True), 
        db.Column('tag_id', db.Integer, 
        db.ForeignKey('tags.id'), primary_key=True))

a_user_items = db.Table("user_items", 
                    db.Column('user_id', db.Integer,
                    db.ForeignKey('users.id'), primary_key=True), 
                    db.Column('item_id', db.Integer,
                    db.ForeignKey('items.id'), primary_key=True))

# ----------------------------------------------------------------------

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(120), unique=True, nullable=False)
    alt_email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False, server_default='false')
    isBanned = db.Column(db.Boolean, default=False, nullable=False, server_default='false')

    posts = db.relationship("Items", secondary=a_user_items, back_populates="user")
    
    def __repr__(self):
        return f"User('{self.netid}')"

    def myItems(self):
        active_items = Items.query.filter((Items.user.any(netid = self.netid)) & (Items.isActive==True)).all()
        inactive_items = Items.query.filter((Items.user.any(netid = self.netid)) & (Items.isActive==False)).all()
        return active_items, inactive_items

# ----------------------------------------------------------------------

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column('created_date', db.DateTime,
                default=datetime.utcnow)
    end_date = db.Column(db.DateTime,default=(datetime.utcnow() + timedelta(days=DAYS_UNTIL_EXPIRE)))
    isFoundItem = db.Column(db.Boolean)
    isActive = db.Column(db.Boolean, default=True)
    isRenewable = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    picture = db.Column(db.String(255), default = DEFAULT_IMAGE)
    
    categories = db.relationship("Tags", secondary=item_tags,
        back_populates="posts")
    
    isVisible = db.Column(db.Boolean, default = True)

    user = db.relationship("Users", secondary=a_user_items, back_populates="posts")

    def __repr__(self):
        return f"Item name: '{self.title}'"

    def poster(self):
        return self.user

    def all_tags(self):
        location_tags = [tag for tag in self.categories if tag.category == "Location"]
        type_tags = [tag for tag in self.categories if tag.category == "Type"]
        inout_tags = [tag for tag in self.categories if tag.category == "Indoors-Outdoors"]
        return location_tags, type_tags, inout_tags

# ----------------------------------------------------------------------


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    tag_name = db.Column('tag_name', db.String(255))
    category = db.Column('category', db.String(255))

    posts = db.relationship("Items", secondary=item_tags, 
        back_populates="categories")

    def __repr__(self):
        return f"'{self.tag_name}'"

    def listings(self):
        return self.posts
