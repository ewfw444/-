from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.book import Book

def init_db():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.drop_all()
        db.create_all()
        
        # 创建管理员账号
        admin = User(
            username='admin',
            email='admin@library.com',
            is_admin=True
        )
        admin.set_password('admin888')  # 设置管理员密码为 admin888
        db.session.add(admin)
        
        # 添加一些示例图书
        books = [
            Book(
                title='编程入门',
                author='张三',
                isbn='9787111111111',
                quantity=5,
                available=5,
                category='technology'
            ),
            Book(
                title='红楼梦',
                author='曹雪芹',
                isbn='9787111111112',
                quantity=3,
                available=3,
                category='literature'
            ),
            Book(
                title='艺术史',
                author='李四',
                isbn='9787111111113',
                quantity=2,
                available=2,
                category='art'
            )
        ]
        
        for book in books:
            db.session.add(book)
        
        db.session.commit()
        print('Database initialized successfully.')

if __name__ == '__main__':
    init_db() 