
import cv2                                    
import numpy as np  
import pygame
def main1(frame_in):
    #image_path = "F://python_image//fu.png"  
    frame     = frame_in.copy()    
    print     frame.shape   
    cv2.namedWindow("[srcImg]",cv2.WINDOW_AUTOSIZE)
    cv2.imshow("[srcImg]",frame)                  
    a=0
    b=0.6
    c=0.5
    d=1

      
    img_roi_y      = 20                           
    img_roi_x      = 40                             
    img_roi_height = 100                           
    img_roi_width  = 100                           
    
    img_roi        = frame[int(frame.shape[0]*a):int(frame.shape[0]*b),int(frame.shape[1]*c):int(frame.shape[1]*d) ].copy()
    return img_roi
    #img_roi[:100,:]=0

    #cv2.namedWindow("[ROI_Img]",cv2.WINDOW_AUTOSIZE)  
    #cv2.imshow("[ROI_Img]",img_roi)  
    #cv2.imshow("[srcImg_new]",frame)   
    #cv2.imwrite("F://python_image//logo_cut.jpg",img_roi)  
    #cv2.waitKey(0)  
    #cv2.destroyWindow("[srcImg]")                  
    #cv2.destroyWindow("[ROI_Img]")              
    
def main(path):
    cap=cv2.VideoCapture(path)

    ret,frame=cap.read()
    while ret:
        img_roi=main1(frame)
        cv2.imshow("img_roi",img_roi)
        ret,frame=cap.read()
        if cv2.waitKey(1) & 0xff == ord(" "): 
            break
    cv2.destroyAllWindows()

def main3(): 
    pygame.mixer.init()  
    print("play music")  
    track = pygame.mixer.music.load("resource\\warning.wav")  
    pygame.mixer.music.play()  