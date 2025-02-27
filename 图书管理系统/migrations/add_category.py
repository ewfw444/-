from app import create_app, db
from app.models.book import Book
from sqlalchemy import text

def add_category_field():
    app = create_app()
    with app.app_context():
        try:
            # 添加 category 列
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE book ADD COLUMN category VARCHAR(20) DEFAULT "all"'))
                conn.commit()
                print("Successfully added category column")
            
            # 更新现有图书的分类
            books = Book.query.all()
            categories = ['literature', 'technology', 'humanities', 'art', 'life']
            for i, book in enumerate(books):
                book.category = categories[i % len(categories)]
            db.session.commit()
            print("Successfully updated book categories")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    add_category_field() 