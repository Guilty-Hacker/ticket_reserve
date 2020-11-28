from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_constant import HTTP_CREATE_OK
from App.apis.cinema_admin.utils import require_permission
from App.model.cinema_admin.cinema_address_model import CinemaAddress
from App.model.cinema_admin.permissions_constant import PERMISSION_WRITE

"""
    c_user = db.Column(db.Integer,db.ForeignKey(CinemaUser.id))
    name = db.Column(db.String(64))
    city = db.Column(db.String(16))
    district = db.Column(db.String(16))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(32))
"""
parse = reqparse.RequestParser()
parse.add_argument("name",required=True,help="请输入影院名称")
parse.add_argument("city",required=True,help="请输入影院城市")
parse.add_argument("district",required=True,help="请输入影院区域")
parse.add_argument("address",required=True,help="请输入影院详细地址")
parse.add_argument("phone",required=True,help="请输入联系方式")

cinema_fields = {
    "c_user_id":fields.Integer,
    "name":fields.String,
    "city":fields.String,
    "district":fields.String,
    "address":fields.String,
    "phone":fields.String,
    "score":fields.Float,
    "servicecharge":fields.Float,
    "astrict":fields.Float,
    "hallnum":fields.Integer,
}

class CinemaAddressesResource(Resource):
    def get(self):
        return {"msg":"get ok"}
    @require_permission(PERMISSION_WRITE)
    def post(self):
        args = parse.parse_args()
        name = args.get("name")
        city = args.get("city")
        district = args.get("district")
        address = args.get("address")
        phone = args.get("phone")

        cinema_address = CinemaAddress()
        cinema_address.c_user_id = g.user.id
        cinema_address.name = name
        cinema_address.city = city
        cinema_address.district = district
        cinema_address.address = address
        cinema_address.phone = phone

        if not cinema_address.save():
            abort(400,msg="存储失败")
        data = {
            "status":HTTP_CREATE_OK,
            "msg":"影院创建成功",
            "data": marshal(cinema_address,cinema_fields),
        }
        return data

class CinemaAddressResource(Resource):
    def get(self,id):
        pass
    def put(self, id):
        pass
    def pathch(self, id):
        pass
    def delete(self, id):
        pass
