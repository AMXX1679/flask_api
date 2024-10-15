# app/routes.py

from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

# In-memory data store
items = []

@main.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

@main.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@main.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Name is required'}), 400
    item = {
        'id': len(items) + 1,
        'name': data['name']
    }
    items.append(item)
    return jsonify({'item': item}), 201

@main.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify({'item': item})
    else:
        return jsonify({'error': 'Item not found'}), 404

@main.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Name is required'}), 400
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        item['name'] = data['name']
        return jsonify({'item': item})
    else:
        return jsonify({'error': 'Item not found'}), 404

@main.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        items = [itm for itm in items if itm['id'] != item_id]
        return jsonify({'message': 'Item deleted'})
    else:
        return jsonify({'error': 'Item not found'}), 404
