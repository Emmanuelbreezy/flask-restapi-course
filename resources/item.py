from pydoc import describe
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("items", __name__, description="Operations on stores")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, store_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
    
    def put(self, store_id):
        item_data = request.get_json()
        if(
            "price" not in item_data
            or "name" not in item_data
        ):
            abort(404, message="All fields are required")
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
    def get(self, store_id):
        return {"items": list(items.values())}
    
    def post(self, store_id):
        item_data = request.get_json()
        if(
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(404, message="All fields are required")
        
        for item in items.values():
            if(item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]):
                abort(404, message="Item already exists")
                
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id} 
        items[item_id] = item
        return item, 201
    
    