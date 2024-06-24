import streamlit as st  # 导入 Streamlit 库
import pyttsx3  # 导入 pyttsx3 库
import asyncio  # 导入 asyncio 库
import aiohttp  # 导入 aiohttp 库
import numpy as np  # 导入 NumPy 库
import cv2  # 导入 OpenCV 库
import mediapipe as mp  # 导入 MediaPipe 库
import time  # 导入 time 库
from concurrent.futures import ThreadPoolExecutor  # 导入 ThreadPoolExecutor 库

def main():  # 主函数
    st.title("动作监控")  # 设置 Streamlit  title
    st.sidebar.title("控制面板")  # 设置 Streamlit 侧边栏 title
    ip_camera_url_input = st.sidebar.text_input("输入IP摄像头地址:", "http://")  # 创建 IP 摄像头地址输入框
    use_ip_camera_button = st.sidebar.button("使用IP摄像头")  # 创建 使用IP摄像头 按钮
    use_computer_camera_button = st.sidebar.button("使用电脑摄像头")  # 创建 使用电脑摄像头 按钮

    # 添加动作选择下拉框
    exercise_options = {  # 定义动作选项
        "推肩": "shoulder_press",
        "深蹲": "squat",
        "硬拉": "deadlift",
        "卧推": "bench_press"
    }
    selected_exercise = st.sidebar.selectbox("选择健身动作", list(exercise_options.keys()))  # 创建动作选择下拉框

    executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池

    # 初始化pyttsx3引擎
    engine = pyttsx3.init()  # 初始化 pyttsx3 引擎
    engine.setProperty('voice', 'zh')  # 设置语音为中文

    async def query_ollama(prompt):  # 定义异步函数 query_ollama
        url = "http://localhost:11434/v1/chat/completions"  # 设置 API URL
        headers = {  # 设置 headers
            "Content-Type": "application/json",
        }
        data = {  # 设置数据
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "llama3:8b",
            "max_tokens": 80  # 限制最大tokens为80
        }
        async with aiohttp.ClientSession() as session:  # 创建 aiohttp 客户端会话
            async with session.post(url, json=data, headers=headers) as response:  # 发送 POST 请求
                if response.status == 200:  # 如果响应状态码为 200
                    result = await response.json()  # 获取响应 JSON
                    return result.get('choices', [{}])[0].get('message', {}).get('content', '无响应文本')  # 返回响应内容
                else:
                    error_text = await response.text()  # 获取响应文本
                    return f"错误: {response.status} - {error_text}"  # 返回错误信息

    async def evaluate(keypoints, exercise_type):  # 定义异步函数 evaluate
        input_text = (  # 设置输入文本
            f"Evaluate the {exercise_type} keypoints data. Provide direct and concise feedback focusing on form and positioning. "
            f"Control answers within 50 tokens. "
            f"You just answer me how I'm doing. "
            f"Keypoints data: {keypoints}"
        )
        return await query_ollama(input_text)  # 调用 query_ollama 函数

    def run_evaluation(keypoints, exercise_type):  # 定义同步函数 run_evaluation
        loop = asyncio.new_event_loop()  # 创建事件循环
        asyncio.set_event_loop(loop)  # 设置事件循环
        return loop.run_until_complete(evaluate(keypoints, exercise_type))  # 运行 evaluate 函数

    def speak(text):  # 定义语音反馈函数
        engine.say(text)  # 设置语音内容
        engine.runAndWait()  # 等待语音播放完成
        engine.stop()  # 停止语音引擎

    def speak_async(text):  # 定义异步语音反馈函数
        asyncio.get_event_loop().run_in_executor(None, speak, text)  # 在事件循环中运行 speak 函数

    def calculate_calories(count, calories_per_rep=0.1):  # 定义计算卡路里函数
        return count * calories_per_rep  # 返回计算结果

    # 初始化视频源
    cap = None  # 初始化视频捕获对象

    if use_ip_camera_button:  # 如果使用 IP 摄像头按钮被点击
        ip_camera_url = ip_camera_url_input  # 获取 IP 摄像头地址
        try:
            cap = cv2.VideoCapture(ip_camera_url)  # 使用 IP 摄像头的视频源
            if not cap.isOpened():  # 如果视频捕获对象未打开
                st.error("无法打开IP摄像头。请检查URL和网络连接。")  # 显示错误信息
        except Exception as e:  # 捕获异常
            st.error(f"无法打开IP摄像头: {e}")  # 显示错误信息
    elif use_computer_camera_button:  # 如果使用电脑摄像头按钮被点击
        cap = cv2.VideoCapture(0)  # 使用电脑摄像头的视频源

    if cap is not None and cap.isOpened():  # 如果视频捕获对象已打开
        stframe = st.empty()  # 创建 Streamlit 框架
        stsidebar_count = st.sidebar.empty()  # 创建用于显示动作次数的容器
        stsidebar_calories = st.sidebar.empty()  # 创建用于显示卡路里的容器
        stsidebar_timer = st.sidebar.empty()  # 创建用于显示计时器的容器
        st_eval = st.empty()  # 创建用于显示评估结果的容器
        mp_pose = mp.solutions.pose  # 导入 MediaPipe 姿势解决方案
        pose = mp_pose.Pose()  # 创建姿势检测对象

        last_request_time = time.time()  # 记录上次请求时间
        previous_keypoints = None  # 记录上次关键点
        exercise_count = 0  # 初始化动作计数器
        total_calories = 0  # 初始化总消耗卡路里
        start_time = time.time()  # 记录开始时间

        def is_shoulder_press(keypoints):  # 定义检测推肩动作函数
            left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_elbow = keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            left_wrist = keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]

            if left_elbow[1] < left_shoulder[1] and right_elbow[1] < right_shoulder[1]:
                if left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
                    return True
            return False

        def is_squat(keypoints):  # 定义检测深蹲动作函数
            # 添加检测深蹲动作的逻辑
            left_hip = keypoints[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            left_ankle = keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

            if left_knee[1] > left_hip[1] and right_knee[1] > right_hip[1]:
                if left_ankle[1] < left_knee[1] and right_ankle[1] < right_knee[1]:
                    return True
            return False

        def is_deadlift(keypoints):  # 定义检测硬拉动作函数
            # 添加检测硬拉动作的逻辑
            left_hip = keypoints[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            left_ankle = keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            if left_shoulder[1] < left_hip[1] and right_shoulder[1] < right_hip[1]:
                if left_knee[1] < left_hip[1] and right_knee[1] < right_hip[1]:
                    if left_ankle[1] < left_knee[1] and right_ankle[1] < right_knee[1]:
                        return True
            return False

        def is_bench_press(keypoints):  # 定义检测卧推动作函数
            # 添加检测卧推动作的逻辑
            left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_elbow = keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            left_wrist = keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]

            if left_elbow[1] > left_shoulder[1] and right_elbow[1] > right_shoulder[1]:
                if left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
                    return True
            return False

        def keypoints_changed(previous, current, threshold=0.01):  # 定义检测关键点变化函数
            if previous is None:
                return True
            return np.linalg.norm(np.array(previous) - np.array(current)) > threshold

        async def process_frame(last_request_time, previous_keypoints, exercise_count, total_calories, selected_exercise):  # 定义异步处理帧函数
            evaluation = "暂无评估。"  # 初始化默认评估结果
            last_eval_time = time.time()  # 上次评估的时间
            eval_interval = 10  # 每10秒进行一次评估
            while cap.isOpened():  # 如果视频捕获对象已打开
                ret, frame = cap.read()  # 读取视频帧
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换图像颜色空间
                image.flags.writeable = False

                results = pose.process(image)  # 进行姿势检测

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 转换图像颜色空间
                mp.solutions.drawing_utils.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)  # 绘制姿势关键点

                if results.pose_landmarks:
                    keypoints = np.array(
                        [[lmk.x, lmk.y, lmk.z, lmk.visibility] for lmk in results.pose_landmarks.landmark])  # 获取关键点

                    if selected_exercise == "推肩":
                        current_state = is_shoulder_press(keypoints)
                    elif selected_exercise == "深蹲":
                        current_state = is_squat(keypoints)
                    elif selected_exercise == "硬拉":
                        current_state = is_deadlift(keypoints)
                    elif selected_exercise == "卧推":
                        current_state = is_bench_press(keypoints)
                    else:
                        current_state = False

                    current_time = time.time()
                    if current_state and (current_time - last_eval_time > eval_interval or keypoints_changed(previous_keypoints, keypoints)):
                        future = executor.submit(run_evaluation, keypoints.tolist(), exercise_options[selected_exercise])  # 提交评估任务
                        evaluation = await asyncio.wrap_future(future)  # 等待评估结果
                        last_eval_time = current_time  # 更新上次评估的时间
                        exercise_count += 1  # 完成一个标准动作后计数器加1
                        total_calories = calculate_calories(exercise_count)  # 计算总消耗卡路里
                        previous_keypoints = keypoints
                        speak_async(evaluation)  # 异步语音反馈评估结果
                        st_eval.markdown(f"### 评估结果:\n\n{evaluation}")  # 更新评估结果

                    elapsed_time = time.time() - start_time  # 计算已用时间
                    stsidebar_timer.markdown(f"### 已用时间: {int(elapsed_time // 60)}分{int(elapsed_time % 60)}秒")  # 显示计时器

                    stframe.image(image, channels="BGR")  # 显示图像
                    stsidebar_count.markdown(f"### {selected_exercise} 次数: {exercise_count}")  # 显示动作次数
                    stsidebar_calories.markdown(f"### 消耗卡路里: {total_calories:.2f} kcal")  # 显示消耗的卡路里

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

        asyncio.run(process_frame(last_request_time, previous_keypoints, exercise_count, total_calories, selected_exercise))  # 运行异步处理帧函数
    else:
        st.write("请在控制面板中输入IP摄像头地址并点击'使用IP摄像头'按钮，或者点击'使用电脑摄像头'按钮。")

if __name__ == "__main__":
    main()
