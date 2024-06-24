# 从Flask中导入Flask类
from flask import Flask
# 从flask_sqlalchemy中导入SQLAlchemy类
from flask_sqlalchemy import SQLAlchemy

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 定义create_app函数
def create_app():
    # 创建Flask应用实例
    app = Flask(__name__)
    # 从config.Config中加载应用配置
    app.config.from_object('config.Config')

    # 初始化db实例
    db.init_app(app)

    # 在应用上下文中导入routes模块
    with app.app_context():
        from . import routes
        # 创建所有数据库表
        db.create_all()

    # 返回应用实例
    return app
