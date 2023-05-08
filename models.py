"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

    app.app_context().push()


class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text, nullable=False)  # default=default_img_url)

    @property
    def full_name(self):
        """show first and last name"""

        return f"{self.first_name} {self.last_name}"
