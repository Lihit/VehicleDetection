from MotionDetection import MotionDetection
from Test import test

#test.main3()
#image_roi=[0.1,0.3 ,0,1]
image_roi=[0.35,0.5,0.3,1]
#image_roi=[0.3,0.6,0,1]

back_frame_find=150
WarnningTime=30
MotionDetection.main("./resource/new2.mp4",image_roi,WarnningTime,back_frame_find)

