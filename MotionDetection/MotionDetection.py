# -*- coding: utf-8 -*-
from FindBackFrame import FindBackFrame
import numpy as np
import cv2
import operator
import copy

global frame_inter
frame_inter=5

def cal_distance(position1,position2):
    ret=0
    for (a,b) in zip(list(position1),list(position2)):
        ret=ret+np.power(a-b,2)
    return np.sqrt(ret)


class MotionObject(object):
    def __init__(self,name,contours_rect):
        self.name=name
        self.stopframe=0
        self.contours_rect=contours_rect
        self.first_CenterPosition=(contours_rect[0]+contours_rect[2]/2,contours_rect[1]+contours_rect[3]/2)
        self.current_CenterPosition=(contours_rect[0]+contours_rect[2]/2,contours_rect[1]+contours_rect[3]/2)
    def get_name(self):
        return self.name

    def StopFrame_Count(self):
        self.stopframe+=frame_inter

    def get_StopFrame(self):
        return self.stopframe

    def get_contours_rect(self):
        return self.contours_rect

    def get_first_CenterPosition(self):
        return self.first_CenterPosition

    def get_current_CenterPosition(self):
        return self.current_CenterPosition

    def upgradePosition(self,contours_rect):
        self.contours_rect=contours_rect
        self.current_CenterPosition=(contours_rect[0]+contours_rect[2]/2,contours_rect[1]+contours_rect[3]/2)

    def Distance_FirstAndCurrent(self):
        return cal_distance(self.first_CenterPosition,self.current_CenterPosition)    

  
def Dict_upgrade(position,dict):
    distance=[]
    newdict={}
    key_save=[]
    dict_same={}
    for key in dict:
        dis=cal_distance(list(position),list(dict[key].get_current_CenterPosition()))
        distance.append(dis)
        newdict[key]=dis
    for key in newdict:
        if newdict[key]==min(distance):
            dict_same[key]=dict[key].get_StopFrame()
    
    tmp=sorted(dict_same.iteritems(),key=operator.itemgetter(1),reverse=True)
    return (tmp[0][0],min(distance))

def Dict_upgrade_inv(object_cont,object):
    distance=[]
    for i in range(len(object_cont)):
        contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
        position1=(x+w/2,y+h/2)
        position2=object.get_current_CenterPosition()
        dis=cal_distance(list(position1),list(position2))
        distance.append(dis)
    return(np.argmin(distance),min(distance))


def Dict_Stop_upgrade(object_id_move,object_id_stop):
    key_save=[]
    key_save_left=[]
    for key in object_id_move:
        if object_id_stop.has_key(key):
            key_save.append(key)
            #dis=cal_distance(list(object_id_stop[key].get_current_CenterPosition()),list(object_id_move[key].get_current_CenterPosition()))
            dis=abs(object_id_stop[key].get_current_CenterPosition()[0]-object_id_move[key].get_current_CenterPosition()[0])
            if dis<=1:
                object_id_stop[key]=copy.deepcopy(object_id_move[key])
            else:
                del object_id_stop[key]
    for key in object_id_stop:
        if key in key_save:
            continue
        key_save_left.append(key)

    for key in key_save_left:
        del object_id_stop[key]
    
def Dict_move_upgrade(object_id_move,object_id_stop):
    for key in object_id_stop:
        if object_id_move.has_key(key):
            object_id_move[key]=copy.deepcopy(object_id_stop[key])

def abs_diff(background1,background2): 
    image_diff=np.zeros(background2.shape,np.uint8)
    (w,h)=background2.shape
    for i in range(w):
        for j in range(h):
            diff=background2[i,j]-background1[i,j]
            print diff
            if diff<0:
                image_diff[i,j]=0
            else:
                image_diff[i,j]=diff
    return image_diff

def time_count_upgrade(object_id_stop,time_count_dict,frame_inter):
    if object_id_stop=={}:
        return time_count_dict
    if time_count_dict=={}:
        for key in object_id_stop:
            time_frame=0
            time_count_loss=0
            time_name=object_id_stop[key].get_name()
            time_position=object_id_stop[key].get_current_CenterPosition()
            time_tag=[list(time_position),[time_frame,time_count_loss]]
            time_count_dict[time_name]=time_tag
    else:
        key_save=[]
        key_del_save=[]
        for key1 in time_count_dict:
            flag=0
            flag2=0
            for key2 in object_id_stop:
                position1=time_count_dict[key1][0]
                position2=list(object_id_stop[key2].get_current_CenterPosition())
                dis=cal_distance(position1,position2)
                if dis<=50:         
                    key_save.append(key2)
                    flag=1            
                    if time_count_dict[key1][1][1]>0:
                        time_count_dict[key1][1][1]=0       
                    if flag2==0:
                        flag2=1
                        time_count_dict[key1][1][0]+=frame_inter


            if flag==0:
                time_count_dict[key1][1][1]+=1

        for key in object_id_stop:
            if key in key_save:
                continue
            time_frame=0
            time_count_loss=0
            time_name=object_id_stop[key].get_name()
            time_position=object_id_stop[key].get_current_CenterPosition()
            time_tag=[list(time_position),[time_frame,time_count_loss]]
            time_count_dict[time_name]=time_tag

        for key in time_count_dict:
            if time_count_dict[key][1][1]>50:
                key_del_save.append(key)
        for key in key_del_save:
            del time_count_dict[key]
    return time_count_dict

def main(path,image_roi,back_frame_find):
    camera=cv2.VideoCapture(path)
    time_count_dict={}
    global fps
    global a
    global b
    global c
    global d
    a=image_roi[0]
    b=image_roi[1]
    c=image_roi[2]
    d=image_roi[3]

    background1=None
    background2=None

    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    es2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (25,25))

    global object_count;
    object_count=0;
    object_id_move={}
    object_id_stop={}

    frame=FindBackFrame.FindBackFrame(path,back_frame_find)
    cv2.imshow("frame_background_find",frame)

    global frame_background
    fps=int(camera.get(cv2.CAP_PROP_FPS))
    roi_x=int(frame.shape[0]*a)
    roi_y=int(frame.shape[1]*c)
    roi_x1=int(frame.shape[0]*b)
    roi_y1=int(frame.shape[1]*d)
    frame_background=frame[roi_x:roi_x1,roi_y:roi_y1].copy()
    #frame_background=frame[int(frame.shape[0]*a):int(frame.shape[0]*b),:].copy()
    
    cv2.imshow("frame_background",frame_background)

    while(True):
        object_cont=[]
        #print frame_background.shape
        background1=cv2.cvtColor(frame_background.copy(),cv2.COLOR_BGR2GRAY)
        background1=cv2.GaussianBlur(background1,(21,21),0)
        #print background1.shape
        #background3=background1[int(background1.shape[0]*a):int(background1.shape[0]*b),:].copy()
        for i in range(frame_inter):
            ret,frame=camera.read()
            if not ret:
                break

        if not ret:
           break
        frame_background1=frame[roi_x:roi_x1,roi_y:roi_y1].copy()
        #frame_background1=frame[int(frame.shape[0]*a):int(frame.shape[0]*b),:].copy()
        #print frame_background1.shape
        background2=cv2.cvtColor(frame_background1.copy(),cv2.COLOR_BGR2GRAY)
        background2=cv2.GaussianBlur(background2,(21,21),0)
        #print background2.shape
        #background4=background2[int(background2.shape[0]*a):int(background2.shape[0]*b),:].copy()
  
        frame_diff=cv2.absdiff(background1,background2)
        #frame_diff=abs_diff(background1,background2)
        cv2.imshow("frame_diff",frame_diff)
        frame_diff=cv2.medianBlur(frame_diff,5)

        frame_threshold=cv2.threshold(frame_diff,10,255,cv2.THRESH_BINARY)[1]
        cv2.imshow("frame_threshold",frame_threshold)   
 
        frame_dilate = cv2.dilate(frame_threshold, es, iterations = 1)
        #frame_close=cv2.morphologyEx(frame_dilate,cv2.MORPH_CLOSE,es2)
        cv2.imshow("frame_dilate", frame_dilate)

        image,cnts, hierarchy = cv2.findContours(frame_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            cont_area=cv2.contourArea(c)
            if cont_area<2000:
                continue
            object_cont.append(c)

        object_cont_len=len(object_cont)
        if object_cont_len>0:
           if object_cont_len>len(object_id_move) and len(object_id_move)==0:
               for i in range(object_cont_len):
                   contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
                   object_count+=1
                   name="object"+str(object_count)
                   obj_id=MotionObject(name,contours_rect)
                   object_id_move[name]=obj_id
               Dict_Stop_upgrade(object_id_move,object_id_stop)

           elif object_cont_len==len(object_id_move) and len(object_id_move)!=0:
                for i in range(object_cont_len):
                    contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
                    position1=(x+w/2,y+h/2)
                    key_tmp,move_distance=Dict_upgrade(position1,object_id_move)
                    if move_distance==0:
                        object_id_move[key_tmp].upgradePosition(contours_rect)
                        if not object_id_stop.has_key(key_tmp):
                            object_id_stop[key_tmp]=copy.deepcopy(object_id_move[key_tmp])
                    else:
                        object_id_move[key_tmp].upgradePosition(contours_rect)
                Dict_Stop_upgrade(object_id_move,object_id_stop)

           elif object_cont_len<len(object_id_move) and len(object_id_move)!=0:
               key_save=[]
               key_save1=[]
               key_save2=[]
               object_id_tmp2={}
               for key in object_id_move:
                   if not object_id_stop.has_key(key):
                       object_id_tmp2[key]=copy.deepcopy(object_id_move[key])
               object_id_tmp=copy.deepcopy(object_id_tmp2)
               if len(object_id_tmp)==0:
                   for i in range(object_cont_len):
                       contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
                       position1=(x+w/2,y+h/2)
                       key_tmp,move_distance=Dict_upgrade(position1,object_id_move)
                       object_id_move[key_tmp].upgradePosition(contours_rect)
                       key_save1.append(key_tmp)
                   for key in object_id_move:
                       if key in key_save1:
                           continue
                       key_save2.append(key)
                   for key in key_save2:
                       del object_id_move[key]
               else:
                   for i in range(object_cont_len):
                       contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
                       position1=(x+w/2,y+h/2)
                       if len(object_id_tmp)>0:
                           key_tmp,move_distance=Dict_upgrade(position1,object_id_tmp2)
                           if move_distance==0:
                               object_id_move[key_tmp].upgradePosition(contours_rect)
                               if not object_id_stop.has_key(key_tmp):
                                   object_id_stop[key_tmp]=copy.deepcopy(object_id_move[key_tmp])
                               key_save.append(key_tmp)
                               #del object_id_tmp[key_tmp]
                           else:
                               object_id_move[key_tmp].upgradePosition(contours_rect)
                               key_save.append(key_tmp)
                               #del object_id_tmp[key_tmp]
                   for key in object_id_tmp:
                       if key in key_save:
                           continue
                       del object_id_move[key]
               Dict_Stop_upgrade(object_id_move,object_id_stop)

           elif object_cont_len>len(object_id_move) and len(object_id_move)!=0:
               index_save=[]
               for key in object_id_move:
                   index,move_distance=Dict_upgrade_inv(object_cont,object_id_move[key])
                   index_save.append(index)
                   contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[index])
                   if move_distance==0:
                       object_id_move[key].upgradePosition(contours_rect)
                       if not object_id_stop.has_key(key):
                           object_id_stop[key]=copy.deepcopy(object_id_move[key])
                       
                   else:
                       object_id_move[key].upgradePosition(contours_rect)

               for i in range(len(object_cont)):
                   if i in index_save:
                       continue
                   object_count+=1
                   name="object"+str(object_count)
                   contours_rect=(x ,y ,w ,h )=cv2.boundingRect(object_cont[i])
                   obj_id=MotionObject(name,contours_rect)
                   object_id_move[name]=obj_id
               Dict_Stop_upgrade(object_id_move,object_id_stop)
        else:
            object_id_move.clear()
            object_id_stop.clear()
            frame_background=frame_background1.copy()
        
        
        if object_id_stop=={}:
            key_save=[]
            for key in time_count_dict:
                time_count_dict[key][1][0]+=frame_inter
                time_count_dict[key][1][1]+=1
                #print time_count_dict[key][1][1]
                if time_count_dict[key][1][1]>38:
                    key_save.append(key)
            for key in key_save:
                del time_count_dict[key]
        else:
            time_count_dict=time_count_upgrade(object_id_stop,time_count_dict,frame_inter)
        for key in time_count_dict:
            time_s=time_count_dict[key][1][0]/(fps)      
            x=time_count_dict[key][0][0]+roi_y
            y=time_count_dict[key][0][1]+roi_x
            cv2.putText(frame,str(time_s)+" s",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
            print key+":"+str(time_s)+" s"

        #print "object_id_stop"+str(len(object_id_stop))
        for key1 in object_id_stop:
            object_id_stop[key1].StopFrame_Count()
            #StopFrame=object_id_stop[key1].get_StopFrame
            #print object_id_stop[key1].get_name()+":"+str(object_id_stop[key1].get_StopFrame()/fps)+" s"
            Dict_move_upgrade(object_id_move,object_id_stop)
            position=object_id_stop[key1].get_contours_rect()
            x=position[0]
            y=position[1]
            w=position[2]
            h=position[3]
            #print object_id_stop[key2].get_name()+":"+str((x,y))
            #cv2.rectangle(frame_background1,(x,y),(x+w,y+h),(0,0,255),2)
            #cv2.putText(frame_background1,object_id_stop[key1].get_name(),(x,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
            cv2.rectangle(frame,(roi_y+x,roi_x+y),(roi_y+x+w,roi_x+y+h),(0,0,255),2)
            #cv2.putText(frame,object_id_stop[key1].get_name(),(roi_y+x,roi_x+y+h/2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)

        #print "object_id_move"+str(len(object_id_move))
        for key2 in object_id_move:
            if object_id_stop.has_key(key2):
                continue
            position=object_id_move[key2].get_contours_rect()
            x=position[0]
            y=position[1]
            w=position[2]
            h=position[3]
            #print object_id_move[key2].get_name()+":"+str((x,y))
            #cv2.rectangle(frame_background1,(x,y),(x+w,y+h),(0,255,0),2)      
            cv2.rectangle(frame,(roi_y+x,roi_x+y),(roi_y+x+w,roi_x+y+h),(0,255,0),2)
            #cv2.putText(frame,object_id_move[key2].get_name(),(roi_y+x,roi_x+y+h/2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)

        #cv2.imshow("frame_background1",frame_background1)
        cv2.imshow("frame",frame)
        if cv2.waitKey(100) & 0xff == ord(" "): 
            cv2.waitKey(0)
        if cv2.waitKey(100) & 0xff == ord("q"):
             break
    cv2.destroyAllWindows()
    camera.release()        


