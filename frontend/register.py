import streamlit as st  # 导入 Streamlit 库
import requests  # 导入 requests 库

def main():  # 定义主函数
    st.title("注册")  # 设置页面标题

    username = st.text_input("用户名")  # 获取用户名输入
    password = st.text_input("密码", type="password")  # 获取密码输入
    email = st.text_input("电子邮件")  # 获取电子邮件输入
    if st.button("注册"):  # 点击注册按钮
        response = requests.post("http://localhost:5000/register", json={"username": username, "password": password, "email": email})  # 发送注册请求
        if response.status_code == 201:  # 如果注册成功
            st.success("注册成功")  # 显示注册成功信息
        else:  # 如果注册失败
            st.error("注册失败")  # 显示注册失败信息
            st.write(response.status_code)  # 显示响应状态码
            st.write(response.text)  # 打印响应内容以调试
