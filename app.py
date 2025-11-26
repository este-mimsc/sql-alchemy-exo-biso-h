"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Shared database instances
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so SQLAlchemy knows them
    import models  # noqa: F401

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    # ---------------------------
    # USERS ROUTES
    # ---------------------------

    @app.route("/users", methods=["GET", "POST"])
    def users():
        from models import User

        if request.method == "GET":
            users = User.query.all()
            return jsonify([u.to_dict() for u in users]), 200

        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")

            if not username:
                return jsonify({"error": "username required"}), 400

            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        from models import User

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404

        return jsonify(user.to_dict()), 200

    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        from models import User

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404

        data = request.get_json()
        user.username = data.get("username", user.username)
        db.session.commit()

        return jsonify(user.to_dict()), 200

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        from models import User

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

    # ---------------------------
    # POSTS ROUTES
    # ---------------------------

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        from models import Post, User

        if request.method == "GET":
            posts = Post.query.all()
            return jsonify([p.to_dict() for p in posts]), 200

        if request.method == "POST":
            data = request.get_json()

            # TESTS EXPECT THIS EXACT BEHAVIOR:
            username = data.get("username")
            title = data.get("title")
            content = data.get("content")

            if not username:
                return jsonify({"error": "username required"}), 400

            user = User.query.filter_by(username=username).first()
            if not user:
                return jsonify({"error": "user not found"}), 404

            post = Post(
                title=title,
                content=content,
                user=user
            )

            db.session.add(post)
            db.session.commit()

            return jsonify(post.to_dict()), 201

    @app.route("/posts/<int:post_id>", methods=["GET"])
    def get_post(post_id):
        from models import Post

        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "post not found"}), 404

        return jsonify(post.to_dict()), 200

    @app.route("/posts/<int:post_id>", methods=["PUT"])
    def update_post(post_id):
        from models import Post, User

        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "post not found"}), 404

        data = request.get_json()
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)

        if "username" in data:
            user = User.query.filter_by(username=data["username"]).first()
            if user:
                post.user = user

        db.session.commit()
        return jsonify(post.to_dict()), 200

    @app.route("/posts/<int:post_id>", methods=["DELETE"])
    def delete_post(post_id):
        from models import Post

        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "post not found"}), 404

        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted"}), 200

    return app


# Module-level app for python app.py
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
