from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Message
from main import db

def register_routes(app):
    @app.route("/")
    def home():
        if 'user_id' in session:
            return redirect(url_for('chat'))
        return render_template("home.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if len(password) < 6:
                return "Пароль должен быть не менее 6 символов."
            hashed_password = generate_password_hash(password)

            if User.query.filter_by(username=username).first():
                return "Пользователь с таким именем уже существует."

            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("reg.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect(url_for("chat"))
            return "Неверные данные для входа."
        return render_template("lg.html")

    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        if "user_id" not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        users = User.query.filter(User.id != user_id).all()

        if request.method == "POST":
            receiver_id = request.form.get("receiver_id")
            content = request.form.get("content")
            if receiver_id and content:
                new_message = Message(sender_id=user_id, receiver_id=receiver_id, content=content)
                db.session.add(new_message)
                db.session.commit()

        messages = (
            Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id))
            .order_by(Message.id.desc())
            .all()
        )
        return render_template("chat_his.html", users=users, messages=messages)

    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        return redirect(url_for("home"))
