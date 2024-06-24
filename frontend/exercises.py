import streamlit as st  # 导入 Streamlit 库
import requests  # 导入 requests 库

def main():  # 定义 main 函数
    st.title("锻炼动作")  # 设置页面标题

    user_id = st.session_state.get('user_id', None)  # 确保用户已登录并获取用户ID
    if not user_id:  # 如果用户未登录
        st.error("请先登录")  # 显示错误信息
        return  # 终止函数执行

    session_id = st.session_state.get('selected_session_id', None)  # 获取当前锻炼会话ID
    if not session_id:  # 如果没有选择特定的锻炼会话
        st.error("没有选择特定的锻炼会话。")  # 显示错误信息
        return  # 终止函数执行

    st.subheader("记录新锻炼动作")  # 设置子标题
    exercise_name = st.text_input("动作名称")  # 获取动作名称输入
    sets = st.number_input("组数", min_value=0)  # 获取组数输入
    reps = st.number_input("次数", min_value=0)  # 获取次数输入
    rest_time = st.number_input("休息时间（秒）", min_value=0)  # 获取休息时间输入
    if st.button("记录锻炼动作"):  # 如果点击记录锻炼动作按钮
        response = requests.post("http://localhost:5000/create_exercise", json={"session_id": session_id, "exercise_name": exercise_name, "sets": sets, "reps": reps, "rest_time": rest_time})  # 发送 POST 请求
        st.write(response.status_code)  # 显示响应状态码
        st.write(response.text)  # 打印响应内容以调试
        if response.status_code == 201:  # 如果响应状态码为 201
            st.success("锻炼动作记录成功")  # 显示成功信息
        else:  # 如果响应状态码不为 201
            st.error(f"记录锻炼动作失败: {response.json().get('error', '')}")  # 显示错误信息

    st.subheader("我的锻炼动作")  # 设置子标题
    response = requests.get(f"http://localhost:5000/get_exercises/{session_id}")  # 发送 GET 请求
    st.write(response.status_code)  # 显示响应状态码
    st.write(response.text)  # 打印响应内容以调试
    if response.status_code == 200:  # 如果响应状态码为 200
        exercises = response.json()  # 获取锻炼动作列表
        for exercise in exercises:  # 遍历锻炼动作列表
            st.write(f"动作名称: {exercise['exercise_name']}")  # 显示动作名称
            st.write(f"组数: {exercise['sets']}")  # 显示组数
            st.write(f"次数: {exercise['reps']}")  # 显示次数
            st.write(f"休息时间: {exercise['rest_time']} 秒")  # 显示休息时间
            st.write("---")  # 显示分隔符
    else:  # 如果响应状态码不为 200
        st.error(f"获取锻炼动作失败: {response.json().get('error', '')}")  # 显示错误信息

if __name__ == "__main__":  # 如果当前模块是主模块
    main()  # 执行 main 函数

