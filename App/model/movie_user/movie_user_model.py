from werkzeug.security import generate_password_hash, check_password_hash
from App.model.movie_user.model_constant import PERMISSION_NONE

from App.ext import db
from App.model import BaseModel

COMMON_USER = 0
BLACK_USER = 1
VIP_USER = 2


class CinemaUser(BaseModel):
    username = db.Column(db.String(32), unique=True)
    _password = db.Column(db.String(256))
    phone = db.Column(db.String(32), unique=True)
    is_delete = db.Column(db.Boolean, default=False)
    permission = db.Column(db.Integer, default=PERMISSION_NONE)

    @property
    def password(self):
        raise Exception("没有权限查看密码")

    @password.setter
    def password(self, password_value):
        self._password = generate_password_hash(password_value)

    def check_password(self, password_value):
        return check_password_hash(self._password, password_value)

    def check_permission(self, permission):
        if BLACK_USER & self.permission == BLACK_USER:
            return False
        else:
            # self.permission 查找当前用户是否为权限为4
            print(permission)
            print(self.permission)
            return permission & self.permission == permission
