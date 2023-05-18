"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

    app.app_context().push()


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """Info about post."""

        p = self
        return f"<post id={p.id} title={p.title} content={p.content} created={p.created_at} user_id={p.user_id}>"

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

# creates many to many relationship between posts and tags
# posts---<PostTag>---Tag
# this table represents the connection between a post and a tag
# makes it easier to access tags of a post or posts associated with a tag.


class PostTag(db.Model):
    """Post tags"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):

        p = self
        return f"<post id={p.id} tag id={p.tag_id}>"


class Tag(db.Model):
    """available tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    # relationship v
    posts = db.relationship('Post', secondary="post_tags",
                            backref="tags", cascade="all,delete")

    def __repr__(self):
        """Info about tag."""

        p = self
        return f"<id={p.id} name={p.name}>"
