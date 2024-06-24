import streamlit as st  # 导入 Streamlit 库
import requests  # 导入 requests 库
import pandas as pd  # 导入 pandas 库
import matplotlib.pyplot as plt  # 导入 matplotlib 库

def main():  # 定义 main 函数
    st.title("数据分析")  # 设置页面标题

    user_id = st.session_state.get('user_id', None)  # 确保用户已登录并获取用户ID
    if not user_id:  # 如果用户未登录
        st.error("请先登录")  # 显示错误信息
        return  # 退出函数

    response = requests.get(f"http://localhost:5000/get_workout_sessions/{user_id}")  # 发送 GET 请求获取锻炼会话数据
    if response.status_code == 200:  # 如果请求成功
        sessions = response.json()  # 获取响应数据
        if not sessions:  # 如果没有锻炼会话数据
            st.warning("没有锻炼会话数据")  # 显示警告信息
            return  # 退出函数
        
        # 将数据转换为 DataFrame
        df = pd.DataFrame(sessions)  # 创建 DataFrame
        df['session_date'] = pd.to_datetime(df['session_date'])  # 将 session_date 转换为日期时间类型
        
        st.write("### 锻炼会话数据")  # 显示锻炼会话数据标题
        st.dataframe(df)  # 显示 DataFrame
        
        # 绘制图表
        st.write("### 锻炼数据图表")  # 显示锻炼数据图表标题
        
        fig, ax = plt.subplots()  # 创建图表
        ax.plot(df['session_date'], df['calories_burned'], marker='o')  # 绘制折线图
        ax.set_title('Calories Burned Over Time')  # 设置图表标题
        ax.set_xlabel('Date')  # 设置 x 轴标签
        ax.set_ylabel('Calories Burned')  # 设置 y 轴标签
        plt.xticks(rotation=45)  # 设置 x 轴刻度旋转角度
        
        st.pyplot(fig)  # 显示图表
        
    else:  # 如果请求失败
        st.error(f"获取锻炼会话数据失败: {response.json().get('error', '')}")  # 显示错误信息

if __name__ == "__main__":  # 如果当前文件作为主程序运行
    main()  # 执行 main 函数

