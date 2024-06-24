import streamlit as st  # 导入 Streamlit 库
import requests  # 导入 requests 库

def main():  # 定义 main 函数
    st.title("健身计划")  # 设置页面标题

    user_id = st.session_state.get('user_id', None)  # 确保用户已登录并获取用户ID
    if not user_id:  # 如果用户未登录
        st.error("请先登录")  # 显示错误信息
        return  # 终止函数执行

    st.subheader("创建新健身计划")  # 设置子标题
    plan_name = st.text_input("计划名称")  # 获取计划名称
    description = st.text_area("描述")  # 获取计划描述
    if st.button("创建计划"):  # 如果点击创建计划按钮
        response = requests.post("http://localhost:5000/create_fitness_plan_with_llama", json={"user_id": user_id, "plan_name": plan_name, "description": description})  # 发送 POST 请求
        st.write(response.status_code)  # 显示响应状态码
        st.write(response.text)  # 打印响应内容以调试
        if response.status_code == 201:  # 如果响应状态码为 201
            st.success("健身计划创建成功")  # 显示成功信息
            st.write(response.json().get("plan", ""))  # 显示计划信息
        else:  # 如果响应状态码不为 201
            st.error(f"创建计划失败: {response.json().get('error', '')}")  # 显示错误信息

    st.subheader("我的健身计划")  # 设置子标题
    response = requests.get(f"http://localhost:5000/get_fitness_plans/{user_id}")  # 发送 GET 请求
    st.write(response.status_code)  # 显示响应状态码
    st.write(response.text)  # 打印响应内容以调试
    if response.status_code == 200:  # 如果响应状态码为 200
        plans = response.json()  # 获取计划列表
        for plan in plans:  # 遍历计划列表
            st.write(f"计划名称: {plan['plan_name']}")  # 显示计划名称
            st.write(f"描述: {plan['description']}")  # 显示计划描述
            st.write("---")  # 显示分隔符
    else:  # 如果响应状态码不为 200
        st.error(f"获取健身计划失败: {response.json().get('error', '')}")  # 显示错误信息

