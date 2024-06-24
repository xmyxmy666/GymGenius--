import streamlit as st  # 导入 streamlit 库
import requests  # 导入 requests 库

def main():  # 定义主函数
    st.title("锻炼会话")  # 设置页面标题

    user_id = st.session_state.get('user_id', None)  # 获取用户ID
    if not user_id:  # 如果用户ID不存在
        st.error("请先登录")  # 显示错误信息
        return  # 返回

    st.subheader("记录新锻炼会话")  # 显示子标题
    duration = st.number_input("持续时间（分钟）", min_value=0)  # 输入持续时间
    calories_burned = st.number_input("消耗卡路里", min_value=0.0, format="%.2f")  # 输入消耗卡路里
    notes = st.text_area("备注")  # 输入备注
    if st.button("记录锻炼会话"):  # 如果点击了记录按钮
        response = requests.post("http://localhost:5000/create_workout_session", json={"user_id": user_id, "duration": duration, "calories_burned": calories_burned, "notes": notes})  # 发送 POST 请求
        st.write(response.status_code)  # 打印响应状态码
        st.write(response.text)  # 打印响应内容以调试
        if response.status_code == 201:  # 如果响应状态码为 201
            st.success("锻炼会话记录成功")  # 显示成功信息
            session_id = response.json().get("session_id")  # 获取会话ID
            st.session_state['session_id'] = session_id  # 保存 session_id 用于记录锻炼动作
        else:  # 否则
            st.error(f"记录锻炼会话失败: {response.json().get('error', '')}")  # 显示错误信息

    st.subheader("我的锻炼会话")  # 显示子标题
    response = requests.get(f"http://localhost:5000/get_workout_sessions/{user_id}")  # 发送 GET 请求
    st.write(response.status_code)  # 打印响应状态码
    st.write(response.text)  # 打印响应内容以调试
    if response.status_code == 200:  # 如果响应状态码为 200
        sessions = response.json()  # 获取会话列表
        for session in sessions:  # 遍历会话列表
            st.write(f"日期: {session['session_date']}")  # 打印会话日期
            st.write(f"持续时间: {session['duration']} 分钟")  # 打印会话持续时间
            st.write(f"消耗卡路里: {session['calories_burned']} kcal")  # 打印会话消耗卡路里
            st.write(f"备注: {session['notes']}")  # 打印会话备注
            # 添加跳转到锻炼动作记录页面的按钮
            if st.button(f"查看锻炼动作记录 - {session['session_date']}", key=session['id']):  # 如果点击了按钮
                st.session_state['selected_session_id'] = session['id']  # 保存选中的会话ID
                st.session_state['page'] = 'exercises'  # 设置页面为锻炼动作
                st.experimental_rerun()  # 重新运行页面
            st.write("---")  # 打印分隔线
    else:  # 否则
        st.error(f"获取锻炼会话失败: {response.json().get('error', '')}")  # 显示错误信息

if __name__ == "__main__":  # 如果当前模块是主模块
    main()  # 调用主函数
