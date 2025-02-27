import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SECRET_KEY = 'your-secret-key-here'  # 设置一个安全的密钥
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 静态文件配置
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app/static')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'app/templates')
    
    # 分页配置
    BOOKS_PER_PAGE = 12 