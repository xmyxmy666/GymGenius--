# 从 sqlalchemy 导入 create_engine 和 text 模块
from sqlalchemy import create_engine, text

# 替换为您的数据库连接信息，例如用户名、密码、主机和数据库名
db_url = 'mysql+pymysql://root:201575@localhost/smart_fitness?charset=utf8mb4'

# 创建数据库引擎，用于连接数据库
engine = create_engine(db_url)

# SQL 语句，用于创建数据库和表
sql_statements = """
CREATE DATABASE IF NOT EXISTS smart_fitness CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_fitness;

# 创建 users 表，用于存储用户信息
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建 fitness_plans 表，用于存储健身计划
CREATE TABLE IF NOT EXISTS fitness_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建 workout_sessions 表，用于存储健身记录
CREATE TABLE IF NOT EXISTS workout_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INT,
    calories_burned FLOAT,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建 exercises 表，用于存储健身项目
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    exercise_name VARCHAR(100) NOT NULL,
    sets INT,
    reps INT,
    rest_time INT,
    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建 exercise_logs 表，用于存储健身记录详细信息
CREATE TABLE IF NOT EXISTS exercise_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    exercise_id INT NOT NULL,
    sets_completed INT,
    reps_completed INT,
    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

# 连接数据库并执行 SQL 语句
with engine.connect() as conn:
    # 遍历 SQL 语句并执行
    for statement in sql_statements.split(';'):
        if statement.strip():
            conn.execute(text(statement))
    # 提交更改
    conn.commit()

print("数据库表创建成功。")
