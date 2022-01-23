from datetime import datetime, timedelta, date
from itertools import groupby
from operator import attrgetter
from collections import defaultdict

from flask import (request, make_response,
                   render_template, redirect, url_for)
from flask.blueprints import Blueprint
from flask_login import login_required, current_user

from tigerapp.config import RENEWAL_THRESHOLD
from tigerapp.models import Items, Tags
from tigerapp.main.util import not_banned, item_query, get_all_tags, posts_by_tag
#----------------------------------------------------------------------

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/main/static/')

#----------------------------------------------------------------------

@main.route("/", methods=['GET'])
def homepage():
    """
    Route for the homepage.

    Case 1: Logged in: Redirects to Found Feed (/found)
    Case 2: Logged out: Redirects to Splash Page (/)
    """

    if current_user.is_authenticated:
        # Already logged in
        return redirect(url_for('main.found'))

    html = render_template('main/index.html')
    response = make_response(html)
    return response
#----------------------------------------------------------------------

@main.route("/found", methods=['GET'])
@login_required
@not_banned
def found():
    """
    Route for the found feed.

    Renders the found feed page using feed.html template.
    All tags are passed in but posts are not.
    """
    tags_by_category = get_all_tags()

    html = render_template("main/feed.html", posts=[],
                           tags_by_category=tags_by_category,
                           title="Found Items", current_user=current_user)
    response = make_response(html)

    return response
#----------------------------------------------------------------------

@main.route("/foundfeed", methods=['GET'])
@login_required
@not_banned
def found_feed():
    """
    Route for getting all items based on the search query and filters.

    Queries the database using the search query and selected filters
    and returns the items in descending order by time. Uses
    feedcard.html template to render the items.
    """
    # retrieves items based on match with description,
    # title, or location, and date range
    items = item_query(found=True)

    # create sets of tags
    all_ids = []
    for key in request.args.keys():
        if key not in ['keyword', 'time', 'startdate', 'enddate']:
            all_ids.append(int(key))

    category_sets = defaultdict(set)
    for id in all_ids:
        category_sets[Tags.query.filter(Tags.id == id)[0].category].add(id)

    posts = posts_by_tag(all_ids, items, category_sets)

    html = ''
    for post in posts:
        html += render_template('main/feedcard.html',
                                netid=current_user.netid,
                                post=post, current_user=current_user) + '\n'
    if html == '':
        html += "<h3>No matching results<br><span class='h5'>(Consider creating a post!)</span><h3>"
    response = make_response(html)

    return response
#----------------------------------------------------------------------


@main.route("/lost", methods=['GET'])
@login_required
@not_banned
def lost():
    """
    Route for the lost feed.

    Renders the lost feed page using feed.html template.
    All tags are passed in but posts are not.
    """
    tags_by_category = get_all_tags()

    html = render_template("main/feed.html",
                           posts=[],
                           tags_by_category=tags_by_category,
                           title="Lost Items", current_user=current_user)
    response = make_response(html)
    return response
#----------------------------------------------------------------------

@main.route("/lostfeed", methods=['GET'])
@login_required
@not_banned
def lost_feed():
    """
    Route for getting all items based on the search query and filters.

    Queries the database using the search query and selected filters
    and returns the items in descending order by time. Uses
    feedcard.html template to render the items.
    """
    # retrieves items based on match with description,
    # title, or location, and start/end date
    items = item_query(found=False)

    # creating sets of selected tags
    all_ids = []
    for key in request.args.keys():
        if key not in ['keyword', 'time', 'startdate', 'enddate']:
            all_ids.append(int(key))

    category_sets = defaultdict(set)
    for id in all_ids:
        category_sets[Tags.query.filter(Tags.id == id)[0].category].add(id)

    # filtering items by tags
    posts = posts_by_tag(all_ids, items, category_sets)

    # creating and returning html response
    html = ''
    for post in posts:
        html += render_template('main/feedcard.html',
                                netid=current_user.netid,
                                post=post,
                                current_user=current_user) + '\n'
    if html == '':
        html += "<h3>No matching results<br><span class='h5'>(Consider creating a post!)</span><h3>"

    response = make_response(html)

    return response
#----------------------------------------------------------------------

@main.route("/myposts", methods=['GET', 'POST'])
@login_required
@not_banned
def myposts():
    """
    Route for the My Posts page.

    Handles tags and renders the page using the myposts.html template.
    Does not handle posts.
    """
    u_netid = current_user.netid
    threshold_date = datetime.utcnow() + timedelta(days=RENEWAL_THRESHOLD)

    ordered_tags = Tags.query.order_by(
        Tags.category).order_by(Tags.tag_name).all()
    tags_by_category = {k: list(g) for k, g in groupby(
        ordered_tags, attrgetter('category'))}
    html = render_template("main/myposts.html", user=u_netid,
                           threshold_date=threshold_date,
                           posts=[], tags_by_category=tags_by_category,
                           title="My Posts")
    response = make_response(html)
    return response
#----------------------------------------------------------------------

@main.route("/myfeed", methods=['GET'])
@login_required
@not_banned
def myposts_feed():
    """
    Route for getting all items created by user based on 
    the search query and filters.

    Queries the database using the search query and selected filters
    and returns the items in descending order by time. Uses
    mypostscard.html template to render the items.
    """
    u_netid = current_user.netid

    keyword = request.args.get('keyword')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')

    # formatting start and end dates
    startdate = datetime.strptime(
        startdate, '%Y-%m-%d') if startdate else date.min
    enddate = datetime.strptime(enddate, '%Y-%m-%d') if enddate else date.max

    is_active = not request.args.get('history') == 'expired'

    is_found1 = True  # found items
    is_found2 = False  # lost items
    lostfound = request.args.get('lostfound')
    if lostfound == "lost":
        is_found1 = not is_found1
    elif lostfound == "found":
        is_found2 = not is_found2

    items = None
    if not keyword:
        items = Items.query.filter(((Items.user.any(netid=u_netid)) &
                                    (Items.isActive == is_active) &
                                    ((Items.isFoundItem == is_found1) |
                                     (Items.isFoundItem == is_found2))) &
                                   ((Items.created_date >= startdate) &
                                    (Items.created_date <= enddate))).all()
    else:
        keyword = "%{}%".format(keyword)
        items = Items.query.filter(((Items.user.any(netid=u_netid)) &
                                    (Items.isActive == is_active) &
                                    (Items.location.ilike(keyword) |
                                     Items.description.ilike(keyword) |
                                     Items.title.ilike(keyword)) &
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

    posts = posts_by_tag(all_ids, items, category_sets)

    html = ''
    for post in posts:
        html += render_template('main/mypostscard.html', post=post) + '\n'

    response = make_response(html)

    return response
#----------------------------------------------------------------------


@main.route("/about", methods=['GET'])
def about():
    html = render_template("main/about.html")
    return make_response(html)
#----------------------------------------------------------------------


@main.route("/banned", methods=['GET'])
def banned():
    return make_response(render_template("main/banned.html"))
#----------------------------------------------------------------------

@main.route("/tutorial", methods=['GET'])
def tutorial():
    html = render_template("main/tutorial.html")
    return make_response(html)

# Error handling
#----------------------------------------------------------------------

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@main.app_errorhandler(Exception)
@main.app_errorhandler(500)
def internal_error(error):
    # print(error, file=stderr)
    # db.session.rollback()
    return render_template('500.html', error=error), 500


@main.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', error=error), 403
#----------------------------------------------------------------------