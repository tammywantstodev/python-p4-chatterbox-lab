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

@app.route('/')
def home():
    return '<h1>Chatterbox Lab</h1>'

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method=="GET":
        messages=[]
        for message in Message.query.order_by('created_at').all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )

        return response
    
    elif request.method=="POST":
        data = request.get_json()
        new_message=Message(
            body=data["body"],
            username=data["username"]
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201


    

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method=="PATCH":
        data=request.get_json()
        message=Message.query.filter(Message.id==id).first()

        for attr, value in data.items():
            setattr(message, attr, value)
        
        db.session.commit()

        response_dict = message.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response
    
    if request.method=="DELETE":
        message=Message.query.filter(Message.id==id).first()

        db.session.delete(message)
        db.session.commit()

        response = make_response(
            "",
            204
        )

        return response



if __name__ == '__main__':
    app.run(port=5555)
