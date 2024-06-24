# 导入 Streamlit 库，用于构建交互式网页应用程序
import streamlit as st
# 导入登录模块，用于用户登录功能
import frontend.login as login
# 导入仪表盘模块，用于显示用户数据
import frontend.dashboard as dashboard
# 导入注册模块，用于用户注册功能
import frontend.register as register
# 导入健身计划模块，用于管理健身计划
import frontend.fitness_plans as fitness_plans
# 导入锻炼会话模块，用于管理锻炼会话
import frontend.workout_sessions as workout_sessions
# 导入锻炼动作模块，用于管理锻炼动作
import frontend.exercises as exercises
# 导入数据分析模块，用于数据分析和可视化
import frontend.data_analysis as data_analysis

# 侧边栏导航，用于选择不同的页面
st.sidebar.title("导航")
# 选择页面，用于选择不同的功能
page = st.sidebar.radio("选择页面", ["登录", "注册", "动作监控", "健身计划", "锻炼会话", "锻炼动作", "数据分析"])

# 如果没有登录状态，则设置为 False
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 根据选择的页面显示内容
if page == "登录":
    # 设置当前页面为登录页面
    st.session_state['page'] = 'login'
    # 调用登录模块的 main 函数
    login.main()
elif page == "注册":
    # 设置当前页面为注册页面
    st.session_state['page'] = 'register'
    # 调用注册模块的 main 函数
    register.main()
elif page == "动作监控":
    # 如果已经登录，则显示动作监控页面
    if st.session_state['logged_in']:
        st.session_state['page'] = 'dashboard'
        dashboard.main()
    else:
        # 否则，显示错误信息，提示用户登录
        st.error("请先登录")
        login.main()
elif page == "健身计划":
    # 如果已经登录，则显示健身计划页面
    if st.session_state['logged_in']:
        st.session_state['page'] = 'fitness_plans'
        fitness_plans.main()
    else:
        # 否则，显示错误信息，提示用户登录
        st.error("请先登录")
        login.main()
elif page == "锻炼会话":
    # 如果已经登录，则显示锻炼会话页面
    if st.session_state['logged_in']:
        st.session_state['page'] = 'workout_sessions'
        workout_sessions.main()
    else:
        # 否则，显示错误信息，提示用户登录
        st.error("请先登录")
        login.main()
elif page == "锻炼动作":
    # 如果已经登录，则显示锻炼动作页面
    if st.session_state['logged_in']:
        st.session_state['page'] = 'exercises'
        exercises.main()
    else:
        # 否则，显示错误信息，提示用户登录
        st.error("请先登录")
        login.main()
elif page == "数据分析":
    # 如果已经登录，则显示数据分析页面
    if st.session_state['logged_in']:
        st.session_state['page'] = 'data_analysis'
        data_analysis.main()
    else:
        # 否则，显示错误信息，提示用户登录
        st.error("请先登录")
        login.main()
else:
    # 如果选择的页面不存在，则显示错误信息
    st.error("页面不存在")