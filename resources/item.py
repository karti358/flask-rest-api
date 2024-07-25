from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt


from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__)

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin", False):
            abort(401, description="Admin Privilege required...")
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message" : "Deleted successfully"})

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        if item:
            if "name" in item_data:
                item.name = item_data["name"]
            
            if "price" in item_data:
                item.price = item_data["price"]
        else:
            item = ItemModel(id = item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self, ):
        items = ItemModel.query.all()
        return items
    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(500, description="Error occured while inserting item")

        return item
