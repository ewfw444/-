from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.book import Book
from app.models.user import User
from app.extensions import db
from sqlalchemy.orm import joinedload

bp = Blueprint('book', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('book.category', category='all'))

@bp.route('/category/<category>')
@login_required
def category(category):
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # 基础查询
    query = Book.query.options(joinedload(Book.borrowers))
    
    # 根据分类筛选
    if category != 'all':
        query = query.filter_by(category=category)
    
    # 分页
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    books = pagination.items
    
    # 分类信息
    categories = [
        {'id': 'all', 'name': '全部', 'icon': 'fa-globe-asia'},
        {'id': 'literature', 'name': '文学小说', 'icon': 'fa-book-open'},
        {'id': 'technology', 'name': '科技教育', 'icon': 'fa-microscope'},
        {'id': 'humanities', 'name': '人文社科', 'icon': 'fa-landmark'},
        {'id': 'art', 'name': '艺术设计', 'icon': 'fa-palette'},
        {'id': 'life', 'name': '生活休闲', 'icon': 'fa-coffee'}
    ]
    
    return render_template('book/index.html', 
                         books=books, 
                         pagination=pagination,
                         current_category=category,
                         categories=categories)

@bp.route('/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available > 0:
        if current_user not in book.borrowers:
            book.borrowers.append(current_user)
            book.available -= 1
            db.session.commit()
            flash('借阅成功', 'success')
        else:
            flash('您已借阅此书', 'warning')
    else:
        flash('图书暂无库存', 'danger')
    return redirect(url_for('book.index'))

@bp.route('/return/<int:book_id>')
@login_required
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user in book.borrowers:
        book.borrowers.remove(current_user)
        book.available += 1
        db.session.commit()
        flash('图书归还成功', 'success')
    else:
        flash('您未借阅此书', 'warning')
    return redirect(url_for('book.index')) 