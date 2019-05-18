from .. import db
import sqlalchemy as sa


class ForgotPassword(db.Model):
    """ ForgotPassword model for storing password reset hashes. """
    __tablename__ = "forgot_password"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hash = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=sa.func.now())
    user = db.relationship("User")
