import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import os

def start_processing():
    global is_running, process_start_time
    is_running = True
    process_start_time = time.time()

# 停止计时器和帧处理
def stop_processing():
    global is_running
    is_running = False

def calculate_percentage(category_frames, total_frames):
    return (category_frames / total_frames) * 100 if total_frames > 0 else 0


def calculate_angle(v1, v2):
    # 计算角度
    angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.arccos(angle) * 180 / np.pi

    # 判断角度符号
    if angle < 0:
        angle = -angle
    
    return angle

def draw_lines_and_angle(frame, point1, point2, point3):
    # 构建矢量
    v1 = point1 - point2
    v2 = point3 - point2

    # 调用计算角度的方法
    angle = calculate_angle(v1, v2)

    # 连线并显示
    cv2.line(frame, tuple(point1), tuple(point2), (255, 0, 0), 2)
    cv2.line(frame, tuple(point2), tuple(point3), (255, 0, 0), 2)

    return angle


def Judge_position(Elbow_angle, Elbow_position_relative_to_the_shoulder, Hip_angle, Ankle_angle, Knee_angle, Trunk_extension):
    global good_sitting_frames, bad_sitting_frames, not_sitting_frames
    posture_text = ''
    # 根据角度范围输出坐姿分类
    if (
        (90 <= Elbow_angle <= 120) and
        (0 <= Elbow_position_relative_to_the_shoulder <= 20) and
        (90 <= Hip_angle <= 120) and
        (100 <= Ankle_angle <= 120) and
        (90 <= Knee_angle <= 130) and
        (0 <= Trunk_extension <= 30)
    ):
        posture_text = 'Good Sitting'
        good_sitting_frames += 1

    elif not (
        (75 <= Elbow_angle <= 135) and
        (-10 <= Elbow_position_relative_to_the_shoulder <= 30) and
        (75 <= Hip_angle <= 135) and
        (90 <= Ankle_angle <= 130) and
        (70 <= Knee_angle <= 150) and
        (-15 <= Trunk_extension <= 45)
    ):
        posture_text = 'Not Sitting'
        not_sitting_frames += 1

    else:
        posture_text = 'Bad Sitting'
        bad_sitting_frames += 1

    return posture_text

def highlight_point(frame, point, number):
    cv2.circle(frame, tuple(point), 5, (0, 255, 0), -1)
    cv2.putText(frame, number, (point[0] - 20, point[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return

def process_frame(img):
    global is_running, process_start_time, total_frames, good_sitting_frames, bad_sitting_frames, not_sitting_frames, posture_text

    if is_running:
        running_time = time.time() - process_start_time
        if running_time < 15:
                # 记录该帧开始处理的时间
                start_time = time.time()

                # BGR转RGB
                img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # 将RGB图像输入模型，获取预测结果
                results = pose.process(img_RGB)

                # 提取关键点坐标
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    # 获取关键点11、13、15的坐标
                    point_11 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * img.shape[0])])
                    point_13 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * img.shape[0])])
                    point_15 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * img.shape[0])])
                    point_23 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * img.shape[0])])
                    point_25 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * img.shape[0])])
                    point_27 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * img.shape[0])])
                    point_31 = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * img.shape[0])])

                    point_11_Floor = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * img.shape[0])+2])
                    point_23_Ceiling = np.array([int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * img.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * img.shape[0])-2])

                    #标记关键点并标出数字
                    highlight_point(img, point_11, '11')
                    highlight_point(img, point_13, '13')
                    highlight_point(img, point_15, '15')
                    highlight_point(img, point_23, '23')
                    highlight_point(img, point_25, '25')
                    highlight_point(img, point_27, '27')
                    highlight_point(img, point_31, '31')


                    # 调用绘制连线和计算角度的方法
                    Elbow_angle = draw_lines_and_angle(img, point_11, point_13, point_15)
                    Elbow_position_relative_to_the_shoulder = draw_lines_and_angle(img, point_13, point_11, point_11_Floor)
                    Hip_angle = draw_lines_and_angle(img, point_11, point_23, point_25)
                    Ankle_angle = draw_lines_and_angle(img, point_25, point_27, point_31)
                    Knee_angle = draw_lines_and_angle(img, point_23, point_25, point_27)
                    Trunk_extension = draw_lines_and_angle(img, point_11, point_23, point_23_Ceiling)
                    # 显示角度
                    cv2.putText(img, f'Elbow Angle: {Elbow_angle:.2f}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)
                    cv2.putText(img, f'Elbow position: {Elbow_position_relative_to_the_shoulder:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)
                    cv2.putText(img, f'Hip angle: {Hip_angle:.2f}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)
                    cv2.putText(img, f'Ankle angle: {Ankle_angle:.2f}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)
                    cv2.putText(img, f'Knee angle: {Knee_angle:.2f}', (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)
                    cv2.putText(img, f'Trunk extension: {Trunk_extension:.2f}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (193,182,255), 2)

                    Judge_position(Elbow_angle, Elbow_position_relative_to_the_shoulder, Hip_angle, Ankle_angle, Knee_angle, Trunk_extension)


                    scaler = 1
                    # 记录该帧处理完毕的时间
                    end_time = time.time()

                    # 计算每秒处理图像帧数FPS
                    FPS = 1/(end_time - start_time)

                    # 在图像上写FPS数值
                    img = cv2.putText(img, 'FPS  '+str(int(FPS)), (25 * scaler, 50 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
                else:
                    scaler = 1
                    failure_str = 'No Person'
                    img = cv2.putText(img, failure_str, (25 * scaler, 100 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
                    print('从图像中未检测出人体关键点，报错。')


        else:
            total_frames = good_sitting_frames + bad_sitting_frames + not_sitting_frames
            print(f'Total Frames: {total_frames}')
            print(f'Good Sitting Frames: {good_sitting_frames}, Percentage: {calculate_percentage(good_sitting_frames, total_frames):.2f}%')
            print(f'Not Sitting Frames: {not_sitting_frames}, Percentage: {calculate_percentage(not_sitting_frames, total_frames):.2f}%')
            print(f'Bad Sitting Frames: {bad_sitting_frames}, Percentage: {calculate_percentage(bad_sitting_frames, total_frames):.2f}%')
            output_file_path = os.path.expanduser("D:\School\Code\Test\output_log.txt")
            with open(output_file_path, 'a') as output_file:
                output_file.write(f'Total Frames: {total_frames}\n')
                output_file.write(f'Good Sitting Frames: {good_sitting_frames}, Percentage: {calculate_percentage(good_sitting_frames, total_frames):.2f}%\n')
                output_file.write(f'Not Sitting Frames: {not_sitting_frames}, Percentage: {calculate_percentage(not_sitting_frames, total_frames):.2f}%\n')
                output_file.write(f'Bad Sitting Frames: {bad_sitting_frames}, Percentage: {calculate_percentage(bad_sitting_frames, total_frames):.2f}%\n')

            total_frames = 0
            good_sitting_frames = 0
            bad_sitting_frames = 0
            not_sitting_frames = 0
            stop_processing()

    return img

# 处理帧的函数
def process_frames():
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = process_frame(frame)
        cv2.imshow('my_window', frame)

        # 按下 's' 键开始计时和处理帧
        key = cv2.waitKey(1)
        if key == ord('s'):
            start_processing()

        # 按下'q'键或'ESC'退出
        if cv2.waitKey(1) in [ord('q'),27]:
            break

# 初始化关键参数
total_frames = 0
good_sitting_frames = 0
not_sitting_frames = 0
bad_sitting_frames = 0
posture_text = ''
is_running = False
process_start_time = 0

# 初始化MediaPipe Pose
mp_pose = mp.solutions.pose

# 导入绘图函数
mp_drawing = mp.solutions.drawing_utils 

# 导入模型
pose = mp_pose.Pose(static_image_mode=False,
                    model_complexity=0, 
                    smooth_landmarks=True,
                    min_detection_confidence=0.5, 
                    min_tracking_confidence=0.5)

# 初始化摄像头
# 打开摄像头
cap = cv2.VideoCapture(0)

# 设置视频质量为1080p 60FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.open(0)


# 使用线程处理帧
frame_processing_thread = threading.Thread(target=process_frames)
frame_processing_thread.start()

# 等待线程完成
frame_processing_thread.join()

# 释放资源
cap.release()
pose.close()
cv2.destroyAllWindows()