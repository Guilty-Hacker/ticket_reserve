import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_constant import HTTP_CREATE_OK, USER_ACTION_LOGIN, USER_ACTION_REGISTER, HTTP_OK
from App.apis.movie_user.model_utils import get_movie_user
from App.ext import cache
from App.model.cinema_admin.cinema_user_model import CinemaUser
from App.utils import generate_movie_user_token

parser_base = reqparse.RequestParser()
parser_base.add_argument("password", type=str, required=True, help="请输入密码")
parser_base.add_argument("action", type=str, required=True, help="请确认请求参数")

parser_register = parser_base.copy()

parser_register.add_argument("username", type=str, required=True, help="请输入用户名")
parser_register.add_argument("phone", type=str, required=True, help="请输入手机号")

parser_login = parser_base.copy()
parser_login.add_argument("username", type=str,help="请输入用户名")
parser_login.add_argument("phone", type=str,help="请输入手机号")

movie_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
    "phone": fields.String,
}

single_movie_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(movie_user_fields)
}


class MovieUsersResource(Resource):
    def post(self):
        args = parser_base.parse_args()

        password = args.get("password")

        action = args.get("action").lower()

        if action == USER_ACTION_REGISTER:
            args_register = parser_register.parse_args()
            username = args_register.get("username")
            phone = args_register.get("phone")
            movie_user = CinemaUser()
            movie_user.username = username
            movie_user.password = password
            movie_user.phone = phone

            if not movie_user.save():
                abort(400, msg="创建用户失败")
            data = {
                "status": HTTP_CREATE_OK,
                "msg": "用户创建成功",
                "data": movie_user,
            }
            return marshal(data, single_movie_user_fields)
        elif action == USER_ACTION_LOGIN:
            args_login = parser_login.parse_args()

            username = args_login.get("username")
            phone = args_login.get("phone")
            user = get_movie_user(phone)
            if not user:
                user = get_movie_user(username)
            if not user:
                abort(400, msg="用户不存在")
            if not user.check_password(password):
                abort(401, msg="用户名或密码错误")
            if user.is_delete:
                abort(401, msg="用户不存在")
            token = generate_movie_user_token()
            cache.set(token, user.id, timeout=60 * 60 * 24 * 7)
            data = {
                "msg": "success",
                "status": HTTP_OK,
                "token": token,
            }
            return data
        else:
            abort(400, msg="参数错误")
