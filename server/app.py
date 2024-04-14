from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return jsonify(messages), 200 
    
    elif request.method == 'POST':
        data = request.json
        username = data.get('username')
        body = data.get('body')

        if not username or not body:
            return jsonify({"error": "Username and body are required"}), 422

        new_message = Message(username=username, body=body)

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        return jsonify(message_dict), 201
    
@app.route('/messages/<int:id>',methods= ['PATCH','DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    if request.method == 'PATCH':
        data = request.json
        new_body = data.get('body')

        if not new_body:
            return jsonify({"error": "New body is required"}), 422

        message.body = new_body
        db.session.commit()

        message_dict = message.to_dict()

        return jsonify(message_dict), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted"
        }

        return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555)