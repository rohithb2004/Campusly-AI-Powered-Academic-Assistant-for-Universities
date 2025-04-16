import json
from flask import Flask
from models import db, Intent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    with open("intents.json", "r") as f:
        data = json.load(f)

    count_added = 0
    for intent in data["intents"]:
        tag = intent["tag"]
        responses = intent["responses"]

        for resp in responses:
            exists = Intent.query.filter_by(tag=tag, response=resp).first()
            if not exists:
                new_intent = Intent(tag=tag, response=resp)
                db.session.add(new_intent)
                count_added += 1

    db.session.commit()
    print(f"✅ Synced {count_added} new responses from intents.json to the database!")
