import cv2
from threading import Thread

class CV2_engine():
    def __init__(self, model):

        self.model = model
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # open camer
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')) # set codec
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # set width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # set height
        self.cap.set(cv2.CAP_PROP_FPS, 60) # set fps

        self.img = None
        self.success = False
        self.model.img = self.img
        self.model.success = self.success
        self.model.camera_stop = False

        self.thread = Thread(target=self.read_camera, args=())
        self.thread.daemon = True
        self.thread.start()

    def read_camera(self):
        while not self.model.camera_stop:
            self.success, self.img = self.cap.read()
            self.model.img = self.img
            self.model.success = self.success
            if self.model.camera_stop:
                break            
           
    def display_camera(self, img=None):
        if img is None:
            cv2.imshow("Image", self.img)
        else:
            cv2.imshow("Image", img)

    def check_exit(self):
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Image',cv2.WND_PROP_VISIBLE) < 1: # if press q
            return True
        else:
            return False    
    
    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()