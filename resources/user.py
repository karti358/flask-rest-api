from flask import request, jsonify, abort
from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jti, get_jwt_identity

from db import db
from models import UserModel, BlockListModel
from schemas import UserSchema

blp = Blueprint("users", __name__)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            return jsonify({"message" : "Username is already registered with us."})
        
        password = pbkdf2_sha256.hash(user_data["password"])
        user = UserModel(username = user_data["username"], password = password)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            return jsonify({"message" : "Could not register. Try Later"})
        
        return jsonify({"message" : "User Created successfully"})

@blp.route("/login")
class UserLogin(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({
                "access_token" : access_token,
                "refresh_token" : refresh_token
                }), 200
        
        abort(401, description="Invalid credentials.")

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self, ):
        refresh_token = request.headers.get("Refresh-Token", False)
        if not refresh_token:
            abort(400, description="Please provide the refresh token...")
        
        jti = get_jwt()["jti"]
        refresh_jti = get_jti(refresh_token)

        blocked_token = BlockListModel(expired_token = jti)
        blocked_refresh_token = BlockListModel(expired_token=refresh_jti)
        try:
            db.session.add(blocked_token)
            db.session.add(blocked_refresh_token)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description="Could not logout successfully...")
        
        return jsonify({"message" : "Logout successful..."}), 200
    

@blp.route("/refresh")
class UserRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self, ):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        
        jti=get_jwt()["jti"]
        blocked = BlockListModel.query.filter(BlockListModel.expired_token==jti)
        try:
            db.session.add(blocked)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description="Database insertion error...")
        
        return jsonify({
            "access_token" : access_token
        }), 200
        