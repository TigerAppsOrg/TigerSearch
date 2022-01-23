from flask import current_app, session
import functools
from flask_login import current_user

# wrapper function for admin
def admin_required(fn):
    @functools.wraps(fn)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        if not current_user.isAdmin:
            return current_app.login_manager.unauthorized()   
        if not session['admin_status']:
            return current_app.login_manager.unauthorized()      
        return fn(*args, **kwargs)
    return decorated_view
