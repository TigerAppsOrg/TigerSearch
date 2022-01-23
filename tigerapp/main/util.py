# ----------------------------------------------------------------------
# Utility functions used in the main package of the application.
# ----------------------------------------------------------------------
import functools
from datetime import datetime, date
from itertools import groupby
from operator import attrgetter

from flask_login import current_user
from flask import redirect, url_for, session, request

from tigerapp.models import Users, Items, Tags
#----------------------------------------------------------------------

# wrapper function for identifying user types
def not_banned(fn):
    @functools.wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_user.isBanned:
            return redirect(url_for('users.logout'))      
        return fn(*args, **kwargs)
    return decorated_view
#----------------------------------------------------------------------

# function for querying the database for items
def item_query(found):

    # arguments from request
    keyword = request.args.get('keyword')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    time_sort = request.args.get('time')

    # convert to datetime
    startdate = datetime.strptime(
        startdate, '%Y-%m-%d') if startdate else date.min
    enddate = datetime.strptime(enddate, '%Y-%m-%d') if enddate else date.max

    items = None
    # qury all
    if not keyword:
        items = Items.query.filter(((Items.isFoundItem == found) &
                                    (Items.isActive == True)) &
                                   ((Items.created_date >= startdate) &
                                    (Items.created_date <= enddate))).all()
    # search by keyword
    else:
        keyword = "%{}%".format(keyword)

        if current_user.isAdmin and session['admin_status']:
            items = Items.query.filter(((Items.isFoundItem == found) &
                                        (Items.isActive == True) &
                                        (Items.location.ilike(keyword) |
                                         Items.description.ilike(keyword) |
                                         Items.title.ilike(keyword) | Items.user.any(Users.netid.ilike(keyword)))) &
                                       ((Items.created_date >= startdate) &
                                        (Items.created_date <= enddate))).all()
        else:
            items = Items.query.filter(((Items.isFoundItem == found) &
                                        (Items.isActive == True) &
                                        (Items.location.ilike(keyword) |
                                         Items.description.ilike(keyword) |
                                         Items.title.ilike(keyword))) &
                                       ((Items.created_date >= startdate) &
                                        (Items.created_date <= enddate))).all()

    # sort items by date
    items.sort(key=lambda item: item.created_date,
               reverse=(time_sort == "desc" or not time_sort))
    
    return items
#----------------------------------------------------------------------

def get_all_tags():
    ordered_tags = Tags.query.order_by(
        Tags.category).order_by(Tags.tag_name).all()
    tags_by_category = {k: list(g) for k, g in groupby(
        ordered_tags, attrgetter('category'))}
    
    return tags_by_category

def posts_by_tag(all_ids, items, category_sets):
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
    return posts
