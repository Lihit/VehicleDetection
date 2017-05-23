from MotionDetection import MotionDetection
from Test import test

#test.main3()
#image_roi选择图像区域
#image_roi=[0.1,0.3 ,0,1]
image_roi=[0.35,0.5,0.3,1]
#image_roi=[0.3,0.6,0,1]
#startframe选择开始的帧用来做背景
#startframe=500
#back_frame_find是用于寻找背景帧设置的参数

back_frame_find=150
WarnningTime=30
MotionDetection.main("F://python_image//new2.mp4",image_roi,WarnningTime,back_frame_find)

