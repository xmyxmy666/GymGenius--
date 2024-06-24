from flask import Blueprint, request, jsonify  # 导入 Flask 相关模块
from backend import db, bcrypt  # 导入数据库和密码哈希模块
from backend.models import User, FitnessPlan, WorkoutSession, Exercise  # 导入用户、健身计划、锻炼会话和锻炼动作模型
import aiohttp  # 导入异步 HTTP 客户端模块
import asyncio  # 导入异步编程模块

bp = Blueprint('routes', __name__)  # 创建路由蓝图

@bp.route('/register', methods=['POST'])  # 注册路由
def register():
    data = request.get_json()  # 获取请求体 JSON 数据
    username = data.get('username')  # 获取用户名
    password = data.get('password')  # 获取密码
    email = data.get('email')  # 获取电子邮件

    if User.query.filter_by(username=username).first():  # 检查用户名是否已存在
        return jsonify({"error": "用户名已存在"}), 400  # 返回错误响应

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # 哈希密码
    new_user = User(username=username, password_hash=password_hash, email=email)  # 创建新用户
    db.session.add(new_user)  # 添加新用户到数据库
    db.session.commit()  # 提交数据库更改

    return jsonify({"message": "注册成功"}), 201  # 返回成功响应

@bp.route('/login', methods=['POST'])  # 登录路由
def login():
    data = request.get_json()  # 获取请求体 JSON 数据
    username = data.get('username')  # 获取用户名
    password = data.get('password')  # 获取密码

    user = User.query.filter_by(username=username).first()  # 检查用户名是否存在
    if user and bcrypt.check_password_hash(user.password_hash, password):  # 检查密码是否正确
        return jsonify({"message": "登录成功", "user_id": user.id}), 200  # 返回成功响应
    else:
        return jsonify({"error": "用户名或密码错误"}), 401  # 返回错误响应


async def query_llama(prompt):  # 异步 llama 查询函数
    url = "http://localhost:11434/v1/chat/completions"  # 设置 llama API URL
    headers = {
        "Content-Type": "application/json",  # 设置请求头
    }
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt  # 设置 llama 输入文本
            }
        ],
        "model": "llama3:8b",  # 设置 llama 模型
        "max_tokens": 150  # 设置最大 tokens 数量
    }
    async with aiohttp.ClientSession() as session:  # 创建异步 HTTP 客户端会话
        async with session.post(url, json=data, headers=headers) as response:  # 发送 POST 请求
            if response.status == 200:  # 检查响应状态码
                result = await response.json()  # 解析响应 JSON 数据
                return result.get('choices', [{}])[0].get('message', {}).get('content', '无响应文本')  # 返回 llama 响应文本
            else:
                error_text = await response.text()  # 获取响应错误文本
                return f"错误: {response.status} - {error_text}"  # 返回错误响应


@bp.route('/create_fitness_plan_with_llama', methods=['POST'])  # 创建健身计划路由
def create_fitness_plan_with_llama():
    try:
        data = request.get_json()  # 获取请求体 JSON 数据
        user_id = data.get('user_id')  # 获取用户 ID
        plan_name = data.get('plan_name')  # 获取计划名称
        description = data.get('description')  # 获取计划描述

        # 生成 Llama3 8b 模型输入文本
        prompt = f"为以下用户生成一个健身计划:\n\n个人信息: {description}\n\n计划名称: {plan_name}"

        # 通过 asyncio 运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        generated_plan = loop.run_until_complete(query_llama(prompt))  # 运行 llama 查询函数

        # 创建新计划并存储到数据库
        new_plan = FitnessPlan(user_id=user_id, plan_name=plan_name, description=generated_plan)
        db.session.add(new_plan)
        db.session.commit()

        return jsonify({"message": "健身计划创建成功", "plan": generated_plan}), 201  # 返回成功响应
    except Exception as e:
        print(f"Error creating fitness plan with Llama: {e}")  # 打印错误信息
        return jsonify({"error": f"创建健身计划失败: {str(e)}"}), 500  # 返回错误响应

@bp.route('/get_fitness_plans/<int:user_id>', methods=['GET'])  # 获取健身计划路由
def get_fitness_plans(user_id):
    try:
        plans = FitnessPlan.query.filter_by(user_id=user_id).all()  # 获取用户的所有健身计划
        plans_list = [{"id": plan.id, "plan_name": plan.plan_name, "description": plan.description} for plan in plans]  # 将计划列表转换为 JSON 格式
        return jsonify(plans_list), 200  # 返回成功响应
    except Exception as e:
        print(f"Error getting fitness plans: {e}")  # 打印错误信息
        return jsonify({"error": f"获取健身计划失败: {str(e)}"}), 500  # 返回错误响应

@bp.route('/create_workout_session', methods=['POST'])  # 创建锻炼会话路由
def create_workout_session():
    try:
        data = request.get_json()  # 获取请求体 JSON 数据
        user_id = data.get('user_id')  # 获取用户 ID
        duration = data.get('duration')  # 获取锻炼时长
        calories_burned = data.get('calories_burned')  # 获取燃烧卡路里
        notes = data.get('notes')  # 获取备注

        new_session = WorkoutSession(user_id=user_id, duration=duration, calories_burned=calories_burned, notes=notes)  # 创建新锻炼会话
        db.session.add(new_session)
        db.session.commit()

        return jsonify({"message": "锻炼会话记录成功", "session_id": new_session.id}), 201  # 返回成功响应
    except Exception as e:
        print(f"Error creating workout session: {e}")  # 打印错误信息
        return jsonify({"error": f"创建锻炼会话失败: {str(e)}"}), 500  # 返回错误响应

@bp.route('/get_workout_sessions/<int:user_id>', methods=['GET'])  # 获取锻炼会话路由
def get_workout_sessions(user_id):
    try:
        sessions = WorkoutSession.query.filter_by(user_id=user_id).all()  # 获取用户的所有锻炼会话
        sessions_list = [
            {
                "id": session.id,
                "session_date": session.session_date,
                "duration": session.duration,
                "calories_burned": session.calories_burned,
                "notes": session.notes
            } for session in sessions
        ]  # 将锻炼会话列表转换为 JSON 格式
        return jsonify(sessions_list), 200  # 返回成功响应
    except Exception as e:
        print(f"Error getting workout sessions: {e}")  # 打印错误信息
        return jsonify({"error": f"获取锻炼会话失败: {str(e)}"}), 500  # 返回错误响应


@bp.route('/create_exercise', methods=['POST'])  # 创建锻炼动作路由
def create_exercise():
    try:
        data = request.get_json()  # 获取请求体 JSON 数据
        session_id = data.get('session_id')  # 获取锻炼会话 ID
        exercise_name = data.get('exercise_name')  # 获取锻炼动作名称
        sets = data.get('sets')  # 获取组数
        reps = data.get('reps')  # 获取重复次数
        rest_time = data.get('rest_time')  # 获取休息时间

        new_exercise = Exercise(session_id=session_id, exercise_name=exercise_name, sets=sets, reps=reps, rest_time=rest_time)  # 创建新锻炼动作
        db.session.add(new_exercise)
        db.session.commit()

        return jsonify({"message": "锻炼动作记录成功"}), 201  # 返回成功响应
    except Exception as e:
        print(f"Error creating exercise: {e}")  # 打印错误信息
        return jsonify({"error": f"创建锻炼动作失败: {str(e)}"}), 500  # 返回错误响应

@bp.route('/get_exercises/<int:session_id>', methods=['GET'])  # 获取锻炼动作路由
def get_exercises(session_id):
    try:
        exercises = Exercise.query.filter_by(session_id=session_id).all()  # 获取锻炼会话下的所有锻炼动作
        exercises_list = [{"id": exercise.id, "exercise_name": exercise.exercise_name, "sets": exercise.sets, "reps": exercise.reps, "rest_time": exercise.rest_time} for exercise in exercises]  # 将锻炼动作列表转换为 JSON 格式
        return jsonify(exercises_list), 200  # 返回成功响应
    except Exception as e:
        print(f"Error getting exercises: {e}")  # 打印错误信息
        return jsonify({"error": f"获取锻炼动作失败: {str(e)}"}), 500  # 返回错误响应
