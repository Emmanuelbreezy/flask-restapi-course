import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on stores")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
            
            
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data):
        try:
            item = items[item_id]
            item |= item_data
            return item, 200
        except KeyError:
            abort(404, message="Item not found")
            

    def delete(self, store_id):
        try:
            del items[item_id]
            return {"message": "Item deleted successfully"}, 200
        except KeyError:
            abort(404, message="Item not found")
            
            
            
@blp.route("/item")
class ItemList(MethodView):
    
    @blp.response(200, ItemSchema)
    def get(self, store_id):
        return {"items": list(items.values())}
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemUpdateSchema)
    def post(self,item_data):
        for item in items.values():
            if(item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]):
                abort(404, message="Item already exists")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id} 
        items[item_id] = item
        return item, 201
    
    