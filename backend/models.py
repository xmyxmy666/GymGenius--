# 从backend导入db实例
from backend import db
# 从flask_login导入UserMixin实例
from flask_login import UserMixin
# 从werkzeug.security导入generate_password_hash和check_password_hash函数
from werkzeug.security import generate_password_hash, check_password_hash

# 定义User模型
class User(db.Model, UserMixin):
    # 定义id字段，primary_key=True表示该字段为主键
    id = db.Column(db.Integer, primary_key=True)
    # 定义username字段，unique=True表示该字段唯一，nullable=False表示该字段不能为空
    username = db.Column(db.String(50), unique=True, nullable=False)
    # 定义password_hash字段，nullable=False表示该字段不能为空
    password_hash = db.Column(db.String(255), nullable=False)
    # 定义email字段，nullable=True表示该字段可以为空
    email = db.Column(db.String(100), nullable=True)
    # 定义created_at字段，default=db.func.current_timestamp()表示该字段默认值为当前时间戳
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # 定义set_password方法，用于设置用户密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 定义check_password方法，用于检查用户密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 定义__repr__方法，用于返回用户对象的字符串表示
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 定义FitnessPlan模型
class FitnessPlan(db.Model):
    # 定义id字段，primary_key=True表示该字段为主键
    id = db.Column(db.Integer, primary_key=True)
    # 定义user_id字段，ForeignKey='user.id'表示该字段关联User模型的id字段，nullable=False表示该字段不能为空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 定义plan_name字段，nullable=False表示该字段不能为空
    plan_name = db.Column(db.String(100), nullable=False)
    # 定义description字段，nullable=True表示该字段可以为空
    description = db.Column(db.Text, nullable=True)
    # 定义created_at字段，default=db.func.current_timestamp()表示该字段默认值为当前时间戳
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # 定义user关系，backref='fitness_plans'表示该关系的反向引用
    user = db.relationship('User', backref=db.backref('fitness_plans', lazy=True))

    # 定义__repr__方法，用于返回健身计划对象的字符串表示
    def __repr__(self):
        return f"FitnessPlan('{self.plan_name}', '{self.description}')"

# 定义WorkoutSession模型
class WorkoutSession(db.Model):
    # 定义id字段，primary_key=True表示该字段为主键
    id = db.Column(db.Integer, primary_key=True)
    # 定义user_id字段，ForeignKey='user.id'表示该字段关联User模型的id字段，nullable=False表示该字段不能为空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 定义session_date字段，default=db.func.current_timestamp()表示该字段默认值为当前时间戳
    session_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # 定义duration字段，nullable=False表示该字段不能为空
    duration = db.Column(db.Integer, nullable=False)
    # 定义calories_burned字段，nullable=False表示该字段不能为空
    calories_burned = db.Column(db.Float, nullable=False)
    # 定义notes字段，nullable=True表示该字段可以为空
    notes = db.Column(db.Text, nullable=True)

    # 定义user关系，backref='workout_sessions'表示该关系的反向引用
    user = db.relationship('User', backref=db.backref('workout_sessions', lazy=True))

    # 定义__repr__方法，用于返回锻炼会话对象的字符串表示
    def __repr__(self):
        return f"WorkoutSession('{self.duration}', '{self.calories_burned}')"

# 定义Exercise模型
class Exercise(db.Model):
    # 定义id字段，primary_key=True表示该字段为主键
    id = db.Column(db.Integer, primary_key=True)
    # 定义session_id字段，ForeignKey='workout_session.id'表示该字段关联WorkoutSession模型的id字段，nullable=False表示该字段不能为空
    session_id = db.Column(db.Integer, db.ForeignKey('workout_session.id'), nullable=False)
    # 定义exercise_name字段，nullable=False表示该字段不能为空
    exercise_name = db.Column(db.String(100), nullable=False)
    # 定义sets字段，nullable=False表示该字段不能为空
    sets = db.Column(db.Integer, nullable=False)
    # 定义reps字段，nullable=False表示该字段不能为空
    reps = db.Column(db.Integer, nullable=False)
    # 定义rest_time字段，nullable=False表示该字段不能为空
    rest_time = db.Column(db.Integer, nullable=False)

    # 定义session关系，backref='exercises'表示该关系的反向引用
    session = db.relationship('WorkoutSession', backref=db.backref('exercises', lazy=True))

    # 定义__repr__方法，用于返回锻炼动作对象的字符串表示
    def __repr__(self):
        return f"Exercise('{self.exercise_name}', '{self.sets}', '{self.reps}', '{self.rest_time}')"
