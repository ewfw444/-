from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.book import Book
from app.models.user import User
from app.extensions import db

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('您没有管理员权限', 'danger')
        return redirect(url_for('book.index'))
    return render_template('admin/panel.html')

@bp.route('/admin/books', methods=['GET', 'POST'])
@login_required
def manage_books():
    if not current_user.is_admin:
        flash('您没有管理员权限', 'danger')
        return redirect(url_for('book.index'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        
        book = Book(
            title=title, 
            author=author, 
            isbn=isbn,
            quantity=quantity, 
            available=quantity,
            category=category
        )
        db.session.add(book)
        db.session.commit()
        flash('图书添加成功', 'success')
        
    books = Book.query.all()
    return render_template('admin/books.html', books=books)

@bp.route('/admin/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        flash('您没有管理员权限', 'danger')
        return redirect(url_for('book.index'))
    
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.quantity = int(request.form['quantity'])
        book.available = int(request.form['available'])
        book.category = request.form['category']
        
        db.session.commit()
        flash('图书更新成功', 'success')
        return redirect(url_for('admin.manage_books'))
        
    return render_template('admin/edit_book.html', book=book)

@bp.route('/admin/books/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '您没有管理员权限'})
    
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('您没有管理员权限', 'danger')
        return redirect(url_for('book.index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '您没有管理员权限'})
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'success': False, 'message': '不能删除管理员账号'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '您没有管理员权限'})
    
    user = User.query.get_or_404(user_id)
    if user == current_user:
        return jsonify({'success': False, 'message': '不能修改自己的权限'})
    
    user.is_admin = not user.is_admin
    db.session.commit()
    return jsonify({'success': True}) 