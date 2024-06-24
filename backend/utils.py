from werkzeug.security import generate_password_hash, check_password_hash  # 导入密码哈希相关模块

def hash_password(password):  # 定义密码哈希函数
    return generate_password_hash(password)  # 返回密码哈希值

def check_password(hash, password):  # 定义密码检查函数
    return check_password_hash(hash, password)  # 返回密码检查结果
