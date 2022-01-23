from sys import stderr
from datetime import datetime, timedelta

from flask import (make_response, render_template,
                   url_for, flash, redirect, request, abort)
from flask.blueprints import Blueprint
from flask.helpers import url_for
from flask_login import login_required, current_user
from flask import render_template
import cloudinary.uploader
import cloudinary.api
from tigerapp import db
from tigerapp.posts.forms import EditForm, PostForm
from tigerapp.models import Items, Tags
from tigerapp.posts.util import email_url
from tigerapp.main.util import not_banned
from tigerapp.config import DAYS_UNTIL_EXPIRE, DEFAULT_IMAGE

from PIL import Image
import io
# ----------------------------------------------------------------------

posts = Blueprint('posts', __name__, template_folder='templates')

# ----------------------------------------------------------------------


@posts.route('/post/new/<found>', methods=["GET", "POST"])
@login_required
@not_banned
def create_post(found):
    """
    Route for creating a new lost or found post. Uses the PostForm
    from forms.py and the createpost.html template to render the form.
    """

    # uses primary key
    found = True if found == 'found' else False
    location_tags = [(str(item.id), item.tag_name)
                     for item in Tags.query.filter_by(category='Location').all()]
    type_tags = [(str(item.id), item.tag_name)
                 for item in Tags.query.filter_by(category='Type').all()]
    inout_tags = [(str(item.id), item.tag_name)
                  for item in Tags.query.filter_by(category='Indoors-Outdoors').all()]

    form = PostForm()
    form.location_tags.choices = location_tags
    form.type_tags.choices = type_tags
    form.inout_tags.choices = inout_tags

    if form.validate_on_submit():
        new_post = Items(isFoundItem=found,
                         title=form.title.data,
                         description=form.description.data,
                         location=form.location.data,
                         )
        # get Tag with selected id and add to current post
        for ident in form.location_tags.data:
            new_post.categories.append(
                Tags.query.filter(Tags.id == int(ident)).first())

        for ident in form.type_tags.data:
            new_post.categories.append(
                Tags.query.filter(Tags.id == int(ident)).first())

        for ident in form.inout_tags.data:
            new_post.categories.append(
                Tags.query.filter(Tags.id == int(ident)).first())

        if form.upload.data:
            
            # resize image, preserving aspect ratio
            basewidth = 300
            img = Image.open(form.upload.data)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            # convert Image to byte array
            # save exif data if exists
            if "exif" in img.info.keys():
                exif = img.info['exif']
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, 'JPEG', exif=exif)
            else:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, 'PNG')
            a = img_byte_arr.getvalue()
            
            response = cloudinary.uploader.upload_image(a)
            new_post.picture = response.url

        db.session.add(new_post)
        current_user.posts.append(new_post)  # add post to user
        db.session.commit()

        flash("Your post has been created!", "success")
        return redirect(url_for("main.myposts"))

    title = "Create Found Post" if found else "Create Lost Post"
    return make_response(render_template("posts/createpost.html",
                                         title=title, form=form))
# ----------------------------------------------------------------------


@posts.route('/post/<int:post_id>/edit', methods=["GET", "POST"])
@login_required
@not_banned
def edit_post(post_id):
    """
    Route for editing a post. Uses EditForm from forms.py and
    createpost.html as a template. Passes in current values to display
    to the client.
    """

    item = Items.query.get_or_404(post_id)

    # cannot edit if not owner
    if item.poster()[0] != current_user:
        abort(403)
    
    # cannot edit if post is expired or banned
    if not item.isVisible:
        error = "Cannot edit a banned post. Contact tigersearch@princeton.edu for more information."
        return render_template("403.html", error=error)
    elif not item.isActive:
        error = "Cannot edit a resolved post. You can edit it after unresolving it from the MyPosts page."
        return render_template("403.html", error=error)

    location_tags = [(str(item.id), item.tag_name)
                     for item in Tags.query.filter_by(category='Location').all()]
    type_tags = [(str(item.id), item.tag_name)
                 for item in Tags.query.filter_by(category='Type').all()]
    inout_tags = [(str(item.id), item.tag_name)
                  for item in Tags.query.filter_by(category='Indoors-Outdoors').all()]

    form = EditForm()
    form.location_tags.choices = location_tags
    form.type_tags.choices = type_tags
    form.inout_tags.choices = inout_tags
    image = item.picture
    if image == DEFAULT_IMAGE:
        image = None

    if form.validate_on_submit():
        item.isFoundItem = bool(form.isFoundItem.data)
        item.title = form.title.data
        item.description = form.description.data
        item.location = form.location.data

        item.categories = []

        for ident in form.location_tags.data:
            item.categories.append(Tags.query.filter(
                Tags.id == int(ident)).first())

        for ident in form.type_tags.data:
            item.categories.append(Tags.query.filter(
                Tags.id == int(ident)).first())

        for ident in form.inout_tags.data:
            item.categories.append(Tags.query.filter(
                Tags.id == int(ident)).first())
        if form.imageCleared.data:
            item.picture = DEFAULT_IMAGE
        if form.upload.data:
            
            # resize image, preserving aspect ratio
            basewidth = 300
            img = Image.open(form.upload.data)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            # convert Image to byte array
            # save exif data if exists
            if "exif" in img.info.keys():
                exif = img.info['exif']
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, 'JPEG', exif=exif)
            else:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, 'PNG')
            a = img_byte_arr.getvalue()
            
            response = cloudinary.uploader.upload_image(a)
            item.picture = response.url

        db.session.commit()

        flash("Your post has been edited")
        # return to the "post" instead
        return redirect(url_for("main.myposts"))
    
    # populate form with current values
    elif request.method == "GET":
        form = EditForm(isFoundItem=item.isFoundItem,
                        location=item.location,
                        description=item.description,
                        title=item.title)
        form.location_tags.choices = location_tags
        form.type_tags.choices = type_tags
        form.inout_tags.choices = inout_tags
        location_tags, type_tags, inout_tags = item.all_tags()

        form.location_tags.data = [str(item.id) for item in location_tags]
        form.type_tags.data = [str(item.id)for item in type_tags]
        form.inout_tags.data = [str(item.id)for item in inout_tags]
        image = item.picture
        if image == DEFAULT_IMAGE:
            image = None

    return make_response(render_template("posts/createpost.html",
                                         form=form, title="Edit Post",
                                         image=image))
# ----------------------------------------------------------------------


@posts.route('/post/<int:post_id>/resolve', methods=["GET", "POST"])
@login_required
@not_banned
def resolve(post_id):
    """
    Marks a post as resolved. This post will no longer be visible
    from the lost/found feeds and will be moved to the 'history'
    section of the My Posts page. 
    """
    filters = request.args.get('filters')

    item = Items.query.get_or_404(post_id)

    # check poster is current user
    if item.poster()[0] != current_user:
        abort(403)

    item.isActive = False
    db.session.commit()
    flash('Your post has been resolved!', 'success')

    if filters is None:
        filters = ""

    url = url_for('main.myposts_feed') + filters
    return redirect(url)
#----------------------------------------------------------------------

@posts.route('/post/<int:post_id>/unresolve', methods=["GET", "POST"])
@login_required
@not_banned
def unresolve(post_id):
    """
    Unresolves a resolved post. This post will now be visible in the
    lost/found feed and the 'active' section of the My Posts page.
    """
    filters = request.args.get('filters')
    item = Items.query.get_or_404(post_id)

    # check poster is current user
    if item.poster()[0] != current_user:
        abort(403)

    if not item.isVisible:
        abort(403)

    # if post expired already, automatically renew
    if(item.end_date <= datetime.utcnow()):
        item.end_date = datetime.utcnow() + timedelta(days=DAYS_UNTIL_EXPIRE)
        item.isRenewable = False

    item.isActive = True
    db.session.commit()
    flash('Your post has been unresolved!', 'success')
    if filters is None:
        filters = ""

    url = url_for('main.myposts_feed') + filters
    return redirect(url)
#----------------------------------------------------------------------

@posts.route('/post/<int:post_id>/delete', methods=["GET", "POST"])
@login_required
@not_banned
def delete_post(post_id):
    """
    Removes a post from the platform permanently. 
    """
    filters = request.args.get('filters')
    item = Items.query.get_or_404(post_id)

    # check poster is current user
    if item.poster()[0] != current_user:
        abort(403)
    
    if item.isActive:
        abort(403)

    db.session.delete(item)
    db.session.commit()

    if filters is None:
        filters = ""

    url = url_for('main.myposts_feed') + filters
    return redirect(url)
#----------------------------------------------------------------------

@posts.route('/post/<int:post_id>/contact/<mobile>', methods=["GET", "POST"])
@login_required
@not_banned
def contact(post_id, mobile):
    """
    Creates a draft email about the product and redirects the user to
    gmail.
    """
    item = Items.query.get_or_404(post_id)
    mobile = True if mobile == 'True' else False
    url = email_url(item.poster()[0].netid,
                    item.title, item.isFoundItem, mobile)
    return redirect(url)
#----------------------------------------------------------------------

@posts.route('/post/<int:post_id>/renew', methods=["GET", "POST"])
@login_required
@not_banned
def renew(post_id):

    filters = request.args.get('filters')
    item = Items.query.get_or_404(post_id)

    # check poster is current user
    if item.poster()[0] != current_user:
        abort(403)

    if not item.isRenewable:
        abort(403)
    
    item.end_date = datetime.utcnow() + timedelta(days=DAYS_UNTIL_EXPIRE)
    item.isRenewable = False

    db.session.commit()
    flash('Your post has been renewed!', 'success')
    if filters is None:
        filters = ""
    url = url_for('main.myposts_feed') + filters
    return redirect(url)
    
#----------------------------------------------------------------------
# Error handling
#----------------------------------------------------------------------

@posts.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@posts.errorhandler(Exception)
@posts.errorhandler(500)
def internal_error(error):
    # print(error, file=stderr)
    # db.session.rollback()
    return render_template('500.html', error=error), 500


@posts.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', error=error), 403
#----------------------------------------------------------------------