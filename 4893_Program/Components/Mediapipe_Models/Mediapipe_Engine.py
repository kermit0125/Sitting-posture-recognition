import mediapipe
import cv2
import numpy as np
from Components.Mark_calculate.Mark_calculate_angle import Mark_Engine as angle_process
from Components.Posture_Judge.Posture_Judge import Judge_Engine as pj

class mediapipe_pose_engine():
    def __init__(self):
        self.AI_model = mediapipe.solutions.pose
        self.AI_model_initialized = self.AI_model.Pose(
                                    static_image_mode=False,
                                    model_complexity = 2,
                                    min_detection_confidence = 0.5, 
                                    min_tracking_confidence = 0.5,
                                    enable_segmentation = False,
                                    smooth_segmentation = True
                                    )


    def process_image(self, img):
        self.img = img
        try:
            results = self.AI_model_initialized.process(img)
            if results.pose_landmarks:
                self.landmarks = results.pose_landmarks.landmark
                self.point_11 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_SHOULDER].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_SHOULDER].y * img.shape[0])])
                self.point_13 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_ELBOW].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_ELBOW].y * img.shape[0])])
                self.point_15 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_WRIST].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_WRIST].y * img.shape[0])])
                self.point_23 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_HIP].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_HIP].y * img.shape[0])])
                self.point_25 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_KNEE].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_KNEE].y * img.shape[0])])
                self.point_27 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_ANKLE].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_ANKLE].y * img.shape[0])])
                self.point_31 = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_FOOT_INDEX].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_FOOT_INDEX].y * img.shape[0])])

                self.point_11_Floor = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_SHOULDER].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_SHOULDER].y * img.shape[0])+2])
                self.point_23_Ceiling = np.array([int(self.landmarks[self.AI_model.PoseLandmark.LEFT_HIP].x * img.shape[1]), int(self.landmarks[self.AI_model.PoseLandmark.LEFT_HIP].y * img.shape[0])-2])

                self.Elbow_angle = angle_process.draw_lines_and_angle(self.img, self.point_11, self.point_13, self.point_15)

                self.Elbow_position_relative_to_the_shoulder = angle_process.draw_lines_and_angle(self.img, self.point_13, self.point_11, self.point_11_Floor)
                self.Hip_angle = angle_process.draw_lines_and_angle(self.img, self.point_11, self.point_23, self.point_25)
                self.Ankle_angle = angle_process.draw_lines_and_angle(self.img, self.point_25, self.point_27, self.point_31)
                self.Knee_angle = angle_process.draw_lines_and_angle(self.img, self.point_23, self.point_25, self.point_27)
                self.Trunk_extension = angle_process.draw_lines_and_angle(self.img, self.point_11, self.point_23, self.point_23_Ceiling)


                self.posture_text = pj.judge_posture(self.Elbow_angle, self.Elbow_position_relative_to_the_shoulder, self.Hip_angle, self.Ankle_angle, self.Knee_angle, self.Trunk_extension)

            else:
                cv2.putText(img, "No pose detected", (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        except:
            pass
