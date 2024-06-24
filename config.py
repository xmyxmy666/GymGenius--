import os  # 导入 os 模块

SECRET_KEY = os.urandom(24)  # 生成随机密钥
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:201575@localhost/smart_fitness'  # 设置数据库 URI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 设置是否追踪数据库修改
