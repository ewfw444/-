import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, make_response, request
from config import Config
from app.extensions import init_extensions
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 配置静态文件缓存
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1年
    
    @app.after_request
    def add_header(response):
        if 'Cache-Control' not in response.headers:
            if request.path.startswith('/static/'):
                response.headers['Cache-Control'] = 'public, max-age=31536000'
            else:
                response.headers['Cache-Control'] = 'public, max-age=300'
        return response

    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    from app.routes import auth, book, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(admin.bp)
    
    return app 