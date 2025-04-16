from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import json
from chat import get_response
from models import Intent
app = Flask(__name__)
app.secret_key = "s0meRand0mS3cret!"  # <-- Add this line

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For production, keep this in env vars
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- AUTH ROUTES ------------------

@app.route('/')
def home():
    return render_template("login.html")  # Login page
@app.route("/")
def index():
    if "user" in session:
        return render_template("base.html")
    else:
        return redirect("/login")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user:
        session['user_id'] = user.id
        session['role'] = user.role

        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('chat_page'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('home'))
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_intent = request.form.get("intent")
        new_response = request.form.get("response")
        if new_intent and new_response:
            intent = Intent(tag=new_intent, response=new_response)
            db.session.add(intent)
            db.session.commit()
            flash("Intent added to database!", "success")

    # ✅ Show all intents in the admin panel
    intents = Intent.query.all()
    return render_template("admin.html", intents=intents)

    # ✅ Show all intents in the dashboard
    intents = Intent.query.all()
    return render_template("admin.html", intents=intents)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# ---------------- CHATBOT ROUTES ------------------

@app.route('/chat')
def chat_page():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template("base.html")  # Your chatbot frontend

@app.post("/predict")
def predict():
    if 'user_id' not in session:
        return jsonify({'answer': 'Please login first.'})

    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

# ---------------- MAIN ------------------

if __name__ == "__main__":
    app.run(debug=True)