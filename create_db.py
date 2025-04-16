from flask import Flask
from models import db, User ,Intent 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context(): 
    
    # Drop tables (optional, only if you want to reset)
    db.create_all()  # Create tables
    # Add sample intent
    inspector = db.inspect(db.engine)
    print("Tables in DB:", inspector.get_table_names())

    if not Intent.query.filter_by(tag='greeting').first():
        intent = Intent(tag="greeting", response="Hello! How can I help you?")
        db.session.add(intent)
        db.session.commit()

    # Add users
    users_to_add = [
        {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
        {'username': 'RA2211026020024', 'password': 'pass1', 'role': 'user'},
        {'username': 'RA2211026020025', 'password': 'pass2', 'role': 'user'},
        {'username': 'RA2211026020026', 'password': 'pass3', 'role': 'user'}
    ]

    for u in users_to_add:
        existing_user = User.query.filter_by(username=u['username']).first()
        if not existing_user:
            user = User(username=u['username'], password=u['password'], role=u['role'])
            db.session.add(user)

    db.session.commit()
    print("✅ Database created and users added successfully!")
