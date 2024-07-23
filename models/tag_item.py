from db import db

class TagItemsModel(db.Model):
    __tablename__ = "tags_items"

    id=db.Column(db.Integer, primary_key=True)
    item_id=db.Column(db.Integer, db.ForeignKey("items.id", name="Foreign Key for Items"), nullable=False)
    tag_id=db.Column(db.Integer, db.ForeignKey("tags.id", name="Foreign key for tags"), nullable=False)