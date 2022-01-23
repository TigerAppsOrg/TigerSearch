from flask import (make_response, render_template, session,
                   url_for, redirect, request, abort)
from flask.blueprints import Blueprint
from flask_login import current_user, login_required

from datetime import datetime, date, timedelta
from itertools import groupby
from operator import attrgetter
from collections import defaultdict

from tigerapp.admin.util import admin_required
from tigerapp.models import Items, Users, Tags
from tigerapp import db

# ----------------------------------------------------------------------

admin = Blueprint('admin', __name__, template_folder='templates', 
                static_folder='static', static_url_path='/static/admin')

# ----------------------------------------------------------------------


@admin.route('/admin/stats', methods=["GET"])
@admin_required
def status():
    total_items = len(Items.query.all())
    found_active = len(Items.query.filter(((Items.isFoundItem == True) &
                                           (Items.isActive == True))).all())
    found_inactive = len(Items.query.filter(((Items.isFoundItem == True) &
                                             (Items.isActive == False))).all())
    lost_active = len(Items.query.filter(((Items.isFoundItem == False) &
                                          (Items.isActive == True))).all())
    lost_inactive = len(Items.query.filter(((Items.isFoundItem == False) &
                                            (Items.isActive == False))).all())
    hidden = len(Items.query.filter(Items.isVisible == False).all())
    num_users = len(Users.query.all())

    items = Items.query.all()
    users_with_posts = set()
    for item in items:
        users_with_posts.add(item.user[0].netid)
    active_users = len(users_with_posts)

    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    now = datetime(now.year, now.month, now.day, 23, 59, 59)

    items_today = Items.query.filter(
        (Items.created_date < now) & (Items.created_date > start)).all()
    posts_today = len(items_today)

    stats = {'total_items': total_items, 'found_active': found_active,
             'found_inactive': found_inactive, 'lost_active': lost_active,
             'lost_inactive': lost_inactive, 'hidden': hidden,
             'num_users': num_users, 'active_users': active_users,
             'posts_today': posts_today}

    # actual release date
    RELEASE = datetime(2021, 11, 18, 23, 59, 59)
    delta = now - RELEASE
    # interval endpoints are inclusive, so 9 points
    interval = int((delta.days)/8)
    glabel = list()
    gpoints = list()

    interval_day = RELEASE
    for _ in range(9):
        items_interval = Items.query.filter(
            Items.created_date < interval_day).all()
        glabel.append(interval_day.strftime("%m/%d/%Y"))
        gpoints.append(len(items_interval))
        interval_day = interval_day + timedelta(days=interval)

    # add today as last point
    if not ((delta.days/8).is_integer()):
        glabel.append(now.strftime("%m/%d/%Y"))
        gpoints.append(total_items)

    line_data = {"labels": glabel,
                 "data_1": gpoints}

    doughnut_data = {
        "labels": ['Found Unresolved', 'Lost Unresolved', 'Found Resolved', 'Lost Resolved'],
        "data": [found_active, lost_active, found_inactive, lost_inactive]
    }

    html = render_template('dashboard.html', **stats, line_data = line_data, doughnut_data = doughnut_data, title = 'Admin')
    
    return make_response(html)
    
# ----------------------------------------------------------------------
@admin.route('/admin/statsfeed', methods=["GET"])
@admin_required
def status_feed():
    total_items = len(Items.query.all())
    found_active = len(Items.query.filter(((Items.isFoundItem == True) &
                                           (Items.isActive == True))).all())
    found_inactive = len(Items.query.filter(((Items.isFoundItem == True) &
                                             (Items.isActive == False))).all())
    lost_active = len(Items.query.filter(((Items.isFoundItem == False) &
                                          (Items.isActive == True))).all())
    lost_inactive = len(Items.query.filter(((Items.isFoundItem == False) &
                                            (Items.isActive == False))).all())
    hidden = len(Items.query.filter(Items.isVisible == False).all())
    num_users = len(Users.query.all())

    items = Items.query.all()
    users_with_posts = set()
    for item in items:
        users_with_posts.add(item.user[0].netid)
    active_users = len(users_with_posts)

    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    now = datetime(now.year, now.month, now.day, 23, 59, 59)

    items_today = Items.query.filter(
        (Items.created_date < now) & (Items.created_date > start)).all()
    posts_today = len(items_today)

    stats = {'total_items': total_items, 'found_active': found_active,
             'found_inactive': found_inactive, 'lost_active': lost_active,
             'lost_inactive': lost_inactive, 'hidden': hidden,
             'num_users': num_users, 'active_users': active_users,
             'posts_today': posts_today}

    # actual release date
    RELEASE = datetime(2021, 11, 18, 23, 59, 59)
    delta = now - RELEASE
    # interval endpoints are inclusive, so 9 points
    interval = int((delta.days)/8)
    glabel = list()
    gpoints = list()

    interval_day = RELEASE
    for _ in range(9):
        items_interval = Items.query.filter(
            Items.created_date < interval_day).all()
        glabel.append(interval_day.strftime("%m/%d/%Y"))
        gpoints.append(len(items_interval))
        interval_day = interval_day + timedelta(days=interval)

    # add today as last point
    if not ((delta.days/8).is_integer()):
        glabel.append(now.strftime("%m/%d/%Y"))
        gpoints.append(total_items)

    line_data = {"labels": glabel,
                 "data_1": gpoints}

    doughnut_data = {
        "labels": ['Found Unresolved', 'Lost Unresolved', 'Found Resolved', 'Lost Resolved'],
        "data": [found_active, lost_active, found_inactive, lost_inactive]
    }

    html = render_template('stats.html', **stats, line_data = line_data, doughnut_data = doughnut_data)
    
    return make_response(html)

# ----------------------------------------------------------------------
@admin.route('/post/<int:post_id>/togglevisibility/<feed>', methods=["GET", "POST"])
@admin_required
def toggle_visibility(post_id, feed):

    filters = request.args.get('filters')

    item = Items.query.get_or_404(post_id)
    item.isVisible = not item.isVisible
    item.isActive = False
    db.session.commit()

    if filters is None:
        filters = ""

    if feed == "hidden":
        return redirect(url_for('admin.hidden_feed') + filters)

    if feed == "found":
        return redirect(url_for('main.found_feed') + filters)

    return redirect(url_for('main.lost_feed') + filters)
# ----------------------------------------------------------------------


@admin.route('/user/<int:user_id>/toggleban', methods=["GET", "POST"])
@admin_required
def toggle_ban(user_id):

    filters = request.args.get('filters')

    user = Users.query.get_or_404(user_id)

    if user.isAdmin:
        abort(403)

    user.isBanned = not user.isBanned

    items = user.myItems()
    items = items[0] + items[1]

    for item in items:
        item.isActive = False


    db.session.commit()

    if filters is None:
        filters = ""

    return redirect(url_for('admin.users') + filters)

# ----------------------------------------------------------------------


@admin.route('/admin/hiddenposts', methods=["GET"])
@admin_required
def hidden():

    ordered_tags = Tags.query.order_by(
        Tags.category).order_by(Tags.tag_name).all()
    tags_by_category = {k: list(g) for k, g in groupby(
        ordered_tags, attrgetter('category'))}
    html = render_template("hiddenfeed.html",
                           posts=[], tags_by_category=tags_by_category,
                           title="Hidden Posts")
    response = make_response(html)
    return response
# ----------------------------------------------------------------------


@admin.route("/admin/hiddenfeed", methods=['GET'])
@admin_required
def hidden_feed():
    """
    Route for getting all items created by user based on 
    the search query and filters.

    Queries the database using the search query and selected filters
    and returns the items in descending order by time. Uses
    mypostcard.html template to render the items.
    """

    keyword = request.args.get('keyword')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')

    # formatting start and end dates
    startdate = datetime.strptime(
        startdate, '%Y-%m-%d') if startdate else date.min
    enddate = datetime.strptime(enddate, '%Y-%m-%d') if enddate else date.max

    is_found1 = True  # found items
    is_found2 = False  # lost items
    lostfound = request.args.get('lostfound')
    if lostfound == "lost":
        is_found1 = not is_found1
    elif lostfound == "found":
        is_found2 = not is_found2

    items = None
    if not keyword:
        items = Items.query.filter(((Items.isVisible == False) &
                                    ((Items.isFoundItem == is_found1) |
                                     (Items.isFoundItem == is_found2))) &
                                   ((Items.created_date >= startdate) &
                                    (Items.created_date <= enddate))).all()
    else:
        keyword = "%{}%".format(keyword)
        items = Items.query.filter(((Items.isVisible == False) &
                                    (Items.location.ilike(keyword) |
                                     Items.description.ilike(keyword) |
                                     Items.title.ilike(keyword) | Items.user.any(Users.netid.ilike(keyword))) &
                                    ((Items.isFoundItem == is_found1) |
                                     (Items.isFoundItem == is_found2))) &
                                   ((Items.created_date >= startdate) &
                                    (Items.created_date <= enddate))).all()

    time_sort = request.args.get('time')
    if(time_sort == 'desc' or time_sort == 'asc'):
        items.sort(key=lambda item: item.created_date,
                   reverse=(time_sort == "desc"))
    else:
        items.sort(key=lambda item: item.end_date,
                   reverse=(time_sort == "expDesc"))

    all_ids = []
    for key in request.args.keys():
        if key not in ['keyword', 'time', 'startdate', 'enddate', 'lostfound', 'history']:
            all_ids.append(int(key))

    category_sets = defaultdict(set)
    for id in all_ids:
        category_sets[Tags.query.filter(Tags.id == id)[0].category].add(id)

    posts = []
    if len(all_ids):
        for item in items:
            include = True
            item_tags = set([tag.id for tag in item.categories])
            for tags in category_sets.values():
                if not item_tags.intersection(tags):
                    include = False
                    break

            if include:
                posts.append(item)
    else:
        posts = items

    html = ''
    for post in posts:
        html += render_template('item.html', post=post) + '\n'

    response = make_response(html)

    return response
# ----------------------------------------------------------------------
@admin.route("/user/<int:user_id>/assignadmin", methods=['GET', 'POST'])
@admin_required
def assign_priv(user_id):

    if current_user.netid != 'tigersearch':
        abort(403)

    filters = request.args.get('filters')

    user = Users.query.get_or_404(user_id)
    
    if user.isBanned:
        abort(403)

    user.isAdmin = not user.isAdmin

    db.session.commit()

    if filters is None:
        filters = ""

    return redirect(url_for('admin.users') + filters)


# ----------------------------------------------------------------------
@admin.route("/admin/dashboardfeed", methods=['GET'])
@admin_required
def users():
    keyword = request.args.get('keyword')
    banned = request.args.get('banned')
    admin = request.args.get('admin')
    
    users = None
    if not keyword:
        if admin and banned:
            users = Users.query.filter((Users.isAdmin == True) | (Users.isBanned == True)).order_by(Users.netid)
        elif banned:
            users = Users.query.filter(Users.isBanned == True).order_by(Users.netid)
        elif admin: 
            users = Users.query.filter(Users.isAdmin == True).order_by(Users.netid)
        else:
            users = Users.query.order_by(Users.netid)
       
    else:
        keyword = "%{}%".format(keyword)
        if admin and banned:
            users = Users.query.filter(Users.netid.ilike(keyword) & (Users.isAdmin == True) | (Users.isBanned == True)).order_by(Users.netid)
        elif banned:
            users = Users.query.filter(Users.netid.ilike(keyword) & Users.isBanned == True).order_by(Users.netid)
        elif admin: 
            users = Users.query.filter(Users.netid.ilike(keyword) & Users.isAdmin == True).order_by(Users.netid)
        else:
            users = Users.query.filter(Users.netid.ilike(keyword)).order_by(Users.netid)


    html = ''

    for user in users:
        html += render_template('useritem.html', user=user)

    return make_response(html)
# ----------------------------------------------------------------------

@admin.route("/admin/toggle_admin", methods=['GET', 'POST'])
@login_required
def toggle_admin():
    if not current_user.isAdmin:
        return redirect(url_for('main.found'))

    session['admin_status'] = not session['admin_status']
    return redirect(url_for('main.found'))

    
@admin.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@admin.app_errorhandler(Exception)
@admin.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

@admin.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', error=error), 403