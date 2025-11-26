"""Database models for the blog assignment."""

from app import db


class User(db.Model):
    """Represents a user who can author posts."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)

    # One user has many posts
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):  # pragma: no cover
        return f"<User {self.username}>"

    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Post(db.Model):
    """Represents a blog post written by a user."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)

    # Foreign key links Post → User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):  # pragma: no cover
        return f"<Post {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "author": self.author.username if self.author else None,
        }
