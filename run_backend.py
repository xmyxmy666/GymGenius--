# 从 backend 模块中导入 create_app 和 db
from backend import create_app, db
# 从 backend.models 模块中导入 User、FitnessPlan 和 WorkoutSession 模型
from backend.models import User, FitnessPlan, WorkoutSession  # Ensure all necessary models are imported

# 创建应用程序实例
app = create_app()

# 定义根路由
@app.route('/')
def index():
    # 返回欢迎信息
    return "Hello, this is the main route"

# 定义检查数据库路由
@app.route('/check_db')
def check_db():
    try:
        # 查询所有用户
        users = User.query.all()
        # 返回用户数量
        return f"Number of users in the database: {len(users)}"
    except Exception as e:
        # 捕获异常并返回错误信息
        return f"Error querying the database: {e}"

# 如果当前模块是主模块
if __name__ == "__main__":
    try:
        # 运行应用程序
        app.run(debug=True)
    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"Failed to start the server: {e}")
        raise
