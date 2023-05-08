"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def main_page():
    return redirect('/users')


@app.route('/users')
def users_index():
    """show user and info"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/allusers.html', users=users)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit form"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

# handle new user functionality get/post


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """New user form"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """New user submission form"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

# Delete user

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")