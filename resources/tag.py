from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, StoreModel, TagItemsModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", __name__)

@blp.route("/store/<string:store_id>/tag")
class StoreTags(MethodView):
    
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(500, description="Tag with that name already exist.")

        tag = TagModel(store_id=store_id, **tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(500, description=str(err))
        
        return tag

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class ItemTags(MethodView):

    @jwt_required()
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        item=ItemModel.query.get_or_404(item_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description = "An error occurred while inserting the tag.")
        
        return tag
    
    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        item=ItemModel.query.get_or_404(item_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description = "An error occurred while inserting the tag.")
        
        return {
            "message": "Item removed from tag",
            "item" : item,
            "tag": tag
        }


@blp.route("/tag/<string:tag_id>")
class Tags(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @jwt_required(fresh=True)
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag=TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return jsonify({"message" : "Tag deleted."})
        
        abort(
            400,
            description="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )