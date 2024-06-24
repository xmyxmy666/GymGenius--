import streamlit as st  # 导入 Streamlit 库
import requests  # 导入 requests 库

def main():  # 定义 main 函数
    st.title("登录")  # 设置页面标题

    username = st.text_input("用户名")  # 获取用户名输入
    password = st.text_input("密码", type="password")  # 获取密码输入
    if st.button("登录"):  # 点击登录按钮
        response = requests.post("http://localhost:5000/login", json={"username": username, "password": password})  # 发送 POST 请求
        st.write(response.status_code)  # 打印响应状态码
        st.write(response.text)  # 打印响应内容以调试
        if response.status_code == 200:  # 如果响应状态码为 200
            st.success("登录成功")  # 显示登录成功信息
            user_data = response.json()  # 获取响应 JSON 数据
            st.session_state['logged_in'] = True  # 设置登录状态
            st.session_state['user_id'] = user_data['user_id']  # 保存 user_id
        else:
            st.error("登录失败")  # 显示登录失败信息
