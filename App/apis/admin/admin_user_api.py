import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.admin.admin_utils import get_admin_user
from App.apis.api_constant import HTTP_CREATE_OK, USER_ACTION_LOGIN, USER_ACTION_REGISTER, HTTP_OK
from App.ext import cache
from App.model.admin.admin_user_model import AdminUser
from App.setting import ADMINS
from App.utils import generate_admin_user_token

parser_base = reqparse.RequestParser()
parser_base.add_argument("password", type=str, required=True, help="请输入密码")
parser_base.add_argument("action", type=str, required=True, help="请确认请求参数")
parser_base.add_argument("username", type=str, required=True, help="请输入用户名")


admin_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
}

single_admin_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(admin_user_fields)
}


class AdminUsersResource(Resource):
    def post(self):
        args = parser_base.parse_args()
        password = args.get("password")
        action = args.get("action").lower()

        if action == USER_ACTION_REGISTER:
            args_register = parser_base.parse_args()
            username = args_register.get("username")
            admin_user = AdminUser()
            admin_user.username = username
            admin_user.password = password
            if username in ADMINS:
                admin_user.is_super = True
            if not admin_user.save():
                abort(400, msg="创建用户失败")
            data = {
                "status": HTTP_CREATE_OK,
                "msg": "用户创建成功",
                "data": admin_user,
            }
            return marshal(data, single_admin_user_fields)
        elif action == USER_ACTION_LOGIN:
            args_login = parser_base.parse_args()
            username = args_login.get("username")
            user = get_admin_user(username)
            if not user:
                abort(400, msg="用户不存在")
            if not user.check_password(password):
                abort(401, msg="用户名或密码错误")
            if user.is_delete:
                abort(401, msg="用户不存在")
            token = generate_admin_user_token()
            cache.set(token, user.id, timeout=60 * 60 * 24 * 7)
            data = {
                "msg": "success",
                "status": HTTP_OK,
                "token": token,
            }
            return data
        else:
            abort(400, msg="参数错误")
