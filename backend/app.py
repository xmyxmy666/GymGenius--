# 从Flask导入应用程序实例
from flask import Flask
# 从backend.models导入数据库实例
from backend.models import db
# 从backend.routes导入路由实例
from backend.routes import routes

# 定义create_app函数
def create_app():
    # 创建Flask应用程序实例
    app = Flask(__name__)
    # 设置SECRET_KEY配置
    app.config['SECRET_KEY'] = 'your_secret_key'
    # 设置SQLALCHEMY_DATABASE_URI配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:201575@localhost/smart_fitness'
    
    # 初始化数据库实例
    db.init_app(app)

    # 在应用程序上下文中执行数据库操作
    with app.app_context():
        # 创建所有数据库表
        db.create_all()  # 确保数据库表已创建

    # 注册路由蓝图
    app.register_blueprint(routes)

    # 返回应用程序实例
    return app

# 如果当前模块为主模块
if __name__ == "__main__":
    # 创建应用程序实例
    app = create_app()
    # 运行应用程序
    app.run(debug=True)
