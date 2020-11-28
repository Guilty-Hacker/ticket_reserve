from flask import request, g
from flask_restful import abort

from App.apis.cinema_admin.model_utils import get_cinema_user
from App.ext import cache
from App.utils import CINEMA_USER
from App.model.cinema_admin import cinema_user_model

def _verify():
    token = request.args.get("token")
    if not token:
        abort(401, msg="not login")
    user_id = cache.get(token)
    if not user_id:
        abort(401, msg="token不正确")
    if not token.startswith(CINEMA_USER):
        abort(403,msg="非用户")
    user = get_cinema_user(user_id)
    if not user:
        abort(401, msg="用户不存在")
    g.user = user
    g.auth = token


def login_required(fun):
    def wrapper(*args, **kwargs):
        _verify()
        return fun(*args, **kwargs)

    return wrapper


def require_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(*args, **kwargs):
            _verify()
            if not cinema_user_model.CinemaUser.check_cinema_permission(permission):
                abort(403, msg="没有权限")
            return fun(*args, **kwargs)

        return wrapper

    return require_permission_wrapper
