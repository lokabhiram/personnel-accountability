import os
import numpy as np
import cv2 as cv
import Person
import time
from flask import Flask

app = Flask(__name__)
cnt_up=0
cnt_down = 0
count=0

# Function to increment visitor count
def increment_visitor_count():
    global cnt_down
    cnt_down += 1

# Function to reset visitor count
def reset_visitor_count():
    global cnt_down
    cnt_down = 0

# Function to save visitor count to a file
# def save_visitor_count():
#     with open("visitor_count.txt", "w") as f:
#         f.write(str(cnt_down))

# Function to load visitor count from a file
def load_visitor_count():
    global cnt_down
    if os.path.exists("visitor_count.txt"):
        with open("visitor_count.txt", "r") as f:
            cnt_down = int(f.read())

def background_visitor_counter():
    global cnt_down

    # Your existing visitor counter logic here...
    # Remember to call increment_visitor_count() whenever a visitor is detected

    # For example, you might increment the count every time someone crosses a line:
    # if i.going_DOWN(line_down, line_up):
    #     increment_visitor_count()

@app.route('/visitor_count')
def get_visitor_count():
    return "Number of people inside:" + str(count)

if __name__ == '__main__':
    load_visitor_count()  # Load visitor count from file

    # Start Flask app in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'host':'0.0.0.0', 'port': 5000}).start()

    # Start background visitor counter
    try:
        log = open('log.txt', "w")
    except:
        print("Cannot open log file")

    # Input and output counters
    prev_cnt = 0


    cap = cv.VideoCapture("test/test_1.mp4")
    #cap = cv.VideoCapture('Testfiles/TestVideo.avi')
    #cap = cv.VideoCapture("test_1.mp4")  # Use webcam with device index 0

    #camera = PiCamera()
    ##camera.resolution = (160,120)
    ##camera.framerate = 5
    ##rawCapture = PiRGBArray(camera, size=(160,120))
    ##time.sleep(0.1)


    ##cap.set(3,160) #Width
    ##cap.set(4,120) #Height

    for i in range(19):
        print( i, cap.get(i))

    h =300
    w = 402
    frameArea = h*w
    areaTH = frameArea/250
    print( 'Area Threshold', areaTH)


    line_up = int(2*(h/5))
    line_down   = int(3*(h/5))

    up_limit =   int(1*(h/5))
    down_limit = int(4*(h/5))

    print( "Red line y:",str(line_down))
    print( "Blue line y:", str(line_up))
    line_down_color = (255,0,0)
    line_up_color = (0,0,255)
    pt1 =  [0, line_down];
    pt2 =  [w, line_down];
    pts_L1 = np.array([pt1,pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1,1,2))
    pt3 =  [0, line_up];
    pt4 =  [w, line_up];
    pts_L2 = np.array([pt3,pt4], np.int32)
    pts_L2 = pts_L2.reshape((-1,1,2))

    pt5 =  [0, up_limit];
    pt6 =  [w, up_limit];
    pts_L3 = np.array([pt5,pt6], np.int32)
    pts_L3 = pts_L3.reshape((-1,1,2))
    pt7 =  [0, down_limit];
    pt8 =  [w, down_limit];
    pts_L4 = np.array([pt7,pt8], np.int32)
    pts_L4 = pts_L4.reshape((-1,1,2))


    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

    kernelOp = np.ones((3,3),np.uint8)
    kernelOp2 = np.ones((5,5),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)

    #Variables
    font = cv.FONT_HERSHEY_SIMPLEX
    persons = []
    max_p_age = 5
    pid = 1

    while(cap.isOpened()):
    ##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        ret, frame = cap.read()
    ##    frame = image.array

        for i in persons:
            i.age_one() #age every person one frame
    
        fgmask = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)

    
        try:
            ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
            ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)
            #Opening (erode->dilate) para quitar ruido.
            mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
            mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
            #Closing (dilate -> erode) para juntar regiones blancas.
            mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
            mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
        except:
            print('EOF')
            print( 'UP:',cnt_up)
            print ('DOWN:',cnt_down)
            break
        
        
        # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
        contours0, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv.contourArea(cnt)
            if area > areaTH:
                #################
                #   TRACKING    #
                #################
                
                
                M = cv.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x,y,w,h = cv.boundingRect(cnt)

                new = True
                if cy in range(up_limit,down_limit):
                    for i in persons:
                        if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:

                            new = False
                            i.updateCoords(cx,cy)   
                            if i.going_UP(line_down,line_up) == True:
                                cnt_up += 1;
                                #print( "ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                                log.write("ID: "+str(i.getId())+' crossed going up at ' + time.strftime("%c") + '\n')
                            elif i.going_DOWN(line_down,line_up) == True:
                                cnt_down += 1;
                                #print( "ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                                log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                            break
                        count= cnt_down-cnt_up
                        print("Number of people inside", count)
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()
                        if i.timedOut():
                            
                            index = persons.index(i)
                            persons.pop(index)
                            del i     
                    if new == True:
                        p = Person.MyPerson(pid,cx,cy, max_p_age)
                        persons.append(p)
                        pid += 1     
            
                cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
                img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
                #cv.drawContours(frame, cnt, -1, (0,255,0), 3)
                
        #END for cnt in contours0
        
        for i in persons:
    ##        if len(i.getTracks()) >= 2:
    ##            pts = np.array(i.getTracks(), np.int32)
    ##            pts = pts.reshape((-1,1,2))
    ##            frame = cv.polylines(frame,[pts],False,i.getRGB())
    ##        if i.getId() == 9:
    ##            print str(i.getX()), ',', str(i.getY())
            cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
            
    
        str_up = 'UP: '+ str(cnt_up)
        str_down = 'DOWN: '+ str(cnt_down)
        frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        cv.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv.LINE_AA)
        cv.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv.LINE_AA)
    
            
        

        cv.imshow('Frame',frame)
        cv.imshow('Mask',mask)    
        

    ##    rawCapture.truncate(0)
    
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    #END while(cap.isOpened())
        

    log.flush()
    log.close()
    cap.release()
    cv.destroyAllWindows()
