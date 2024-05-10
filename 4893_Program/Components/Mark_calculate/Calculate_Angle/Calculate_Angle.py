import numpy as np

class Calculate_Angle():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.angle = 1

    def Calculate_Angle(self, v1, v2):
        self.angle = np.dot(self.v1, self.v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        self.angle = np.arccos(self.angle) * 180 / np.pi

        # 判断角度符号
        if self.angle < 0:
            self.angle = -self.anglecl