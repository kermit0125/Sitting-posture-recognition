from MVC.EventManager import *
import MVC.View as view
from Components.Calculate_FPS.FPS_Engine import FPS_engine
from Components.CameraIO.CV2_Engine import CV2_engine
from Components.Mediapipe_Models.Mediapipe_Engine import *
from Components.Segmentation.Segmentation_Engine import segmentation_engine
import pygame

class control(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.pageinitilized = False

        self.model.CV2_class = None

    def initialize(self):
        """
        Initialize view.
        """
        self.graphics = view.UI_View(self.evManager, self.model)
        self.graphics.initialize()

    def input_event(self):
        if self.model.start_button.CheckisClicked() == 'clicked':
            self.model.currentstate += 1
            self.evManager.Post(StateChangeEvent(self.model.currentstate))

        self.model.input_event = pygame.event.get()    
        # Called for each game tick. We check our keyboard presses here.

        for event in self.model.input_event:

            # handle window manager closing our window
            if event.type == pygame.QUIT:
                self.model.camera_stop = True
                self.graphics.quit_pygame()
                self.evManager.Post(QuitEvent())

            # handle key down events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.evManager.Post(StateChangeEvent(None))


    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, InitializeEvent):
            self.initialize()

        # if the state is changing, reset the pageinitilized flag
        elif isinstance(event, StateChangeEvent):
            self.pageinitilized = False
            print("State change event")

        elif isinstance(event, TickEvent):
            
            self.model.currentstate = self.model.state.peek()
            if self.pageinitilized == False:
                """
                Initialize new page
                """
                self.graphics.init_page()

                if self.model.CV2_class == None:
                    self.model.CV2_class = CV2_engine(self.model)
                self.model.FPS_class = FPS_engine(self.model)
                if self.model.currentstate == 2:
                    self.model.Mediapipe_pose_class = mediapipe_pose_engine()
                print("New page initialized")
                # self.model.segmentation_class = segmentation_engine()
                
                self.pageinitilized = True
            
            """
            Handle all Business Logic
            """
            
            # Get camera image from CV2
            # self.model.success, self.model.img = self.model.CV2_class.read_camera() # read camera
            
            if self.model.success:
                # Calculate FPS
                self.model.FPS_class.calculate_FPS()

                try:
                    # Mediapipe Pose
                    if self.model.currentstate == 2:
                        self.model.Mediapipe_pose_class.process_image(self.model.img)
                        # self.model.Mediapipe_pose_class.expand_landmark()
                
                    """
                    Tell view to render after all Business Logic
                    """
                    self.graphics.render()

                except Exception as e:
                    print(e)
                    import traceback
                    traceback.print_exc()

                

            self.input_event()
            
            