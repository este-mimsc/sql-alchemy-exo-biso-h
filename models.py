"""Database models for the blog assignment."""

from app import db


class User(db.Model):
    """Represents a user who can author posts."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)

    # TESTS EXPECT THIS RELATIONSHIP NAME
    posts = db.relationship("Post", back_populates="user")

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

    # TESTS EXPECT THE RELATIONSHIP TO BE CALLED 'user'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):  # pragma: no cover
        return f"<Post {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user": self.user.username if self.user else None,
        }
