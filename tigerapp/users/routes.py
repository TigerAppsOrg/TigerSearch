from cas import CASClient
from flask import session, Blueprint, redirect, request, url_for, render_template
from tigerapp.models import Items, Users
from tigerapp import db
from flask_login import login_user, current_user, logout_user, login_required
from tigerapp.config import ADMIN_NETID

users = Blueprint('users', __name__, template_folder = 'templates')

cas_client = CASClient(
    version=3,
    #service_url='http://localhost:5000/login?next=%2Ffound',
    service_url='https://tigersearch.herokuapp.com/login?next=%2Ffound',
    server_url='https://fed.princeton.edu/cas/login'
)

#reference: https://djangocas.dev/blog/python-cas-flask-example/
@users.route('/login')
def login():
    if current_user.is_authenticated and 'username' in session:
        # Already logged in
        return redirect(url_for('main.found'))

    next = request.args.get('next')
    ticket = request.args.get('ticket')
    if not ticket:
        # No ticket, the request come from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return redirect(cas_login_url)

    # user (net id), attributes, pgtiou 
    user, _, _ = cas_client.verify_ticket(ticket)

    if not user:
        # return 'Failed to verify ticket. <a href="/login">Login</a>'
        return redirect(url_for(users.login))
        
    else:  # Login successfully, redirect according `next` query parameter.
        user = user.lower()
        session['username'] = user #netid

        # check if user exists
        new_user = Users.query.filter(Users.netid == user).one_or_none()
        
        if new_user is None:
            new_user = Users(netid = user)

            if user in ADMIN_NETID:
                new_user.isAdmin = True #tigersearch
            db.session.add(new_user)
            db.session.commit()

        if new_user.isAdmin:
            session['admin_status'] = False

        
        login_user(new_user)
        
        if new_user.isBanned:
            return redirect(url_for('main.banned'))

        return redirect(next)

@users.route('/logout')
@login_required
def logout():
    redirect_url = url_for('users.logout_callback', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)

    return redirect(cas_logout_url)

@users.route('/logout_callback')
def logout_callback():
    # redirect from CAS logout request after CAS logout successfully
    session.pop('username', None)
    session.pop('admin_status', None)
    logout_user()
    return redirect(url_for('main.homepage'))

@users.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@users.app_errorhandler(Exception)
@users.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

@users.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', error=error), 403