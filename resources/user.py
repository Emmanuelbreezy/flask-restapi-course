import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schema import UserSchema


blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user  = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if not user:
            abort(401, message="wrong username or password")
        
        if pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "id": user.id,
                "username": user.username,
                "access_token": access_token,
                "refresh_token": refresh_token
                }
        
        abort(401, message="Invalid credentials")
            
@blp.route("/refresh")
class TokenRefresh(MethodView):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
    

@blp.route("/register")
class UserRegister(MethodView):
    
    @blp.response(200, UserSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="username already exists")
            
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
       
       
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Logout successfully"}
         
    
@blp.route("/user/<string:user_id>")
class User(MethodView):
    
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
         
        
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(User)
        db.session.commit()
        
        return {"message": "User deleted successfully"}, 200
         
        