class Judge_Engine():
    def __init__(self, posture_text):
        self.posture_text = posture_text

    def judge_posture(self, Elbow_angle, Elbow_position_relative_to_the_shoulder, Hip_angle, Ankle_angle, Knee_angle, Trunk_extension):
        global good_sitting_frames, bad_sitting_frames, not_sitting_frames
        self.Elbow_angle = Elbow_angle
        self.Elbow_position_relative_to_the_shoulder = Elbow_position_relative_to_the_shoulder
        self.Hip_angle = Hip_angle
        self.Ankle_angle = Ankle_angle
        self.Knee_angle = Knee_angle
        self.Trunk_extension = Trunk_extension
        if (
            (90 <= Elbow_angle <= 120) and
            (0 <= Elbow_position_relative_to_the_shoulder <= 20) and
            (90 <= Hip_angle <= 120) and
            (100 <= Ankle_angle <= 120) and
            (90 <= Knee_angle <= 130) and
            (0 <= Trunk_extension <= 30)
        ):
            self.posture_text = 'Good Sitting'
            good_sitting_frames += 1

        elif not (
            (75 <= Elbow_angle <= 135) and
            (-10 <= Elbow_position_relative_to_the_shoulder <= 30) and
            (75 <= Hip_angle <= 135) and
            (90 <= Ankle_angle <= 130) and
            (70 <= Knee_angle <= 150) and
            (-15 <= Trunk_extension <= 45)
        ):
            self.posture_text = 'Not Sitting'
            not_sitting_frames += 1

        else:
            self.posture_text = 'Bad Sitting'
            bad_sitting_frames += 1
