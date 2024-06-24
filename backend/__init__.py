# 从Flask导入应用程序实例
from flask import Flask
# 从flask_sqlalchemy导入SQLAlchemy实例
from flask_sqlalchemy import SQLAlchemy
# 从flask_bcrypt导入Bcrypt实例
from flask_bcrypt import Bcrypt
# 从flask_login导入LoginManager实例
from flask_login import LoginManager
# 从sqlalchemy导入text实例
from sqlalchemy import text

# 创建SQLAlchemy实例
db = SQLAlchemy()
# 创建Bcrypt实例
bcrypt = Bcrypt()
# 创建LoginManager实例
login_manager = LoginManager()

# 定义create_app函数
def create_app():
    # 创建Flask应用程序实例
    app = Flask(__name__)
    # 从config对象加载应用程序配置
    app.config.from_object('config')

    # 初始化SQLAlchemy实例
    db.init_app(app)
    # 初始化Bcrypt实例
    bcrypt.init_app(app)
    # 初始化LoginManager实例
    login_manager.init_app(app)

    # 从backend.routes导入蓝图
    from backend.routes import bp as routes_bp
    # 注册蓝图
    app.register_blueprint(routes_bp, url_prefix='/') 

    # 在应用程序上下文中执行数据库操作
    with app.app_context():
        try:
            # 创建所有数据库表
            db.create_all()  
            # 添加打印语句以确认数据库连接
            with db.engine.connect() as conn:
                # 执行SELECT语句
                result = conn.execute(text("SELECT 1"))
                # 打印数据库连接成功信息
                print("Database connected successfully.")
                # 打印查询结果
                print(result.fetchone())
        except Exception as e:
            # 打印数据库连接失败信息
            print(f"Database connection failed: {e}")
            # 抛出异常
            raise

    # 返回应用程序实例
    return app
