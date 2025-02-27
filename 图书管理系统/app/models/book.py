from app.extensions import db
from datetime import datetime

# 定义借阅表
borrowings = db.Table('borrowings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('borrow_date', db.DateTime, default=datetime.utcnow),
    db.Column('return_date', db.DateTime)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Integer, default=1)
    category = db.Column(db.String(20), default='all')
    borrowers = db.relationship('User', secondary=borrowings, backref=db.backref('borrowed_books', lazy='dynamic')) 