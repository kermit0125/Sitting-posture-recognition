from Components.Mark_calculate.Calculate_Angle.Calculate_Angle import Calculate_Angle
import cv2

class Mark_Engine():
    def __init__(self):
        self = self

    def draw_lines_and_angle(self, img, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.img = img
        self.v1 = self.point1 - self.point2
        self.v2 = self.point3 - self.point2
        print('2')
        self.angle = Calculate_Angle.Calculate_Angle(self.v1, self.v2)
        cv2.line(self.img, tuple(self.point1), tuple(self.point2), (255, 0, 0), 2)
        cv2.line(self.img, tuple(self.point2), tuple(self.point3), (255, 0, 0), 2)
