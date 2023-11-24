from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def set_password(self, password):
        bcrypt = Bcrypt()
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    @classmethod
    def verify_user(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user and Bcrypt().check_password_hash(user.password, password):
            # Password is correct
            return True
        # Either the user doesn't exist or the password is incorrect
        return False


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    user_username = db.Column(db.String(20), ForeignKey("users.username"))
    user = relationship("User", backref="feedback")
