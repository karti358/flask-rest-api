from db import db

class BlockListModel(db.Model):
    __tablename__ = "blocklist"

    id=db.Column(db.Integer, primary_key=True)
    expired_token=db.Column(db.String(200), unique=True, nullable=False)