import cv2 
import numpy as np

def FindBackFrame(path,frame_inter):
    camera=cv2.VideoCapture(path)
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    es2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (25,25))
    for i in range(13):
        ret, frame = camera.read()
        if not ret:
            return None

    frame_back=None
    while ret:
        frame1=frame.copy()
        background1 = cv2.cvtColor(frame1.copy(), cv2.COLOR_BGR2GRAY)
        background1 = cv2.GaussianBlur(background1, (21, 21), 0)

        ret,frame=camera.read()
        if not ret:
            break
        background2 = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        background2 = cv2.GaussianBlur(background2, (21, 21), 0)
        diff = cv2.absdiff(background1, background2)
        diff = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow("diff2", diff)
        diff = cv2.dilate(diff, es, iterations = 2)
        diff=cv2.morphologyEx(diff,cv2.MORPH_CLOSE,es2)
        image, cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cont_list=[]
        for c in cnts:
            area=cv2.contourArea(c)
            if area<3000:
                continue
            cont_list.append(c)
        if len(cont_list)==0:
            frame_back=frame.copy()
            break
        elif len(cont_list)==1:
            (x,y,w,h)=cv2.boundingRect(cont_list[0])
            frame_back=frame.copy()
            for i in range(frame_inter):
                ret,frame=camera.read()
                if not ret:
                    break
            if not ret:
                break
            frame_roi=frame[y:y+h,x:x+w]
            frame_back[y:y+h,x:x+w]=frame_roi
            break
        else:
            continue
    return frame_back


        