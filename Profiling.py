import math
from random import randint
import cv2
import collections
#Read video from the given path and get its width and height
cap = cv2.VideoCapture('sample.mp4')
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

def dist(x1,x2):
    sol = math.sqrt((x2[0]-x1[0])**2+(x2[1]-x1[1])**2)
    return sol
#Output video format and location
fourcc = cv2.VideoWriter_fourcc('M','P','E','G')
#tracker =cv2.TrackerBoosting_create()
out = cv2.VideoWriter("Output.avi", fourcc, 5.0, (frame_width,frame_height))

#get first two frames of input video
ret, frame1 = cap.read()
ret, frame2 = cap.read()
l=0
print(ret)
#array to hold co-ordinates of vehicles and bullets
bullet_xy = {}
vehicle1_xy = []
vehicle2_xy=[]
vehicle3_xy = []
bullet1_xy =[]
#Code to identify the vehicle contours
diff = cv2.absdiff(frame1, frame2)
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
_, thresh = cv2.threshold(blur, 20 , 255, cv2.THRESH_BINARY)
dilated = cv2.dilate(thresh, None, iterations=3)
_, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
bboxes = [] #dictonary to hold all the bounding box identified
colors = [] #array to hold assign different colours to each vehicle
for contour in contours:
    bbox = cv2.boundingRect(contour)    #draw bounding rectangles around identified contours
    #cv2.imshow("cc",contour)
    (x, y, w, h) = cv2.boundingRect(contour)    #get the coordinates of the rectangle
    if w>40:     #if w>40 identify a rectangle as a vehicle(found by trial and error)
        bboxes.append(bbox)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))


#Creating a MultiTracker Object and giving the inout as above obtained vehicle rectangles
multiTracker = cv2.MultiTracker_create()
for bbox in bboxes:
    tracker =  cv2.TrackerKCF_create()
    multiTracker.add(tracker, frame1, bbox)


while cap.isOpened():   # As long as the video is opened

    # Code to update the frame to track identified vehicles
    _, retval = multiTracker.update(frame1)  # returns the values of the updated frame

    r0 =retval[0]
    r1 =retval[1]
    r2 =retval[2]
    i = 0
    for box in retval:
        (x, y, w, h) = [int(v) for v in box]
        # to create a rectangle, top-left corner and bottom right corner points are needed. p1 and p2 here.
        cv2.rectangle(frame1, (x, y), (x + w, y + h), colors[i], 2, 1)  # Draw rectangle around the vehicles
        cv2.putText(frame1, 'v :' + str(i) + ' : ' + str(int((x))) + "," + str(int((y))), (x - 50, y - 7),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)
        #vehicle_xy.append((((x + w) / 2), ((y + h) / 2)))
        i += 1
        #print(retval[0][1])
        #cv2.putText(frame1, 'center: ' + str(int((x + w) / 2)) + "," + str(int((y + h) / 2)), (x + w, y + h + 7),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        # print("Vehilce :" + str(vehicle_xy))

    # Code to identify and Track the bullets. Very similar to Vehicle Code
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    _, thresh1 = cv2.threshold(blur1, 30, 127, cv2.THRESH_BINARY)
    dilated1 = cv2.dilate(thresh1, None, iterations=3)
    _, contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    z = 0
    for p in contours1:
        (x1, y1, w1, h1) = cv2.boundingRect(p)
        M = cv2.moments(p)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"] -50)
            cY = int(M["m01"] / M["m00"] -50)
        if h1 >5 and h1<10:  #If h<20, classify it as a bullet and draw the rectangle
            cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (255, 255, 0), 2,1)
            z+=1
            cv2.putText(frame1,'Bullet : ' + str(z) + ', l : '+ str(cX) +','+str(cY),(x1,y1-2),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12),2)
            dict1 = {x1:y1}
            key,value = x1,y1
            #print("b : ",dict1)
            if key not in bullet_xy:
                bullet_xy.update(dict1)
                dv0 = dist(r0,(cX,cY))
                dv1 = dist(r1,(cX,cY))
                dv2 = dist(r2,(cX,cY))
                if dv0<=dv1 and dv0<=dv2:
                    vehicle1_xy.append((r0[0], r0[1]))
                    print("bullet " + str(len(bullet_xy)) + " fired from vehicle 0")
                elif dv1<=dv0 and dv1<= dv2:
                    vehicle2_xy.append((r1[0], r1[1]))
                    print("bullet " + str(len(bullet_xy)) + " fired from vehicle 1")
                else:
                    vehicle3_xy.append((r2[0], r2[1]))
                    print("bullet " + str(len(bullet_xy)) + " fired from vehicle 2")
                #vehicle1_xy.append()
                #print("v1: "+ str(vehicle1_xy), "v2: "+ str(vehicle2_xy) + "v3: "+str(vehicle3_xy))
                #print(len(bullet_xy))
                continue
            else:
                if value == bullet_xy[key]:
                    bullet1_xy.append((x1,y1))
                    dv0 = dist(r0, (cX, cY))
                    dv1 = dist(r1, (cX, cY))
                    dv2 = dist(r2, (cX, cY))
                    if dv0 <= dv1 and dv0 <= dv2:
                        if (r0[0],r0[1]) != vehicle1_xy[-1]:
                            vehicle1_xy.append((r0[0], r0[1]))
                            print("additional "+ str(len(bullet1_xy))+" fired from vehicle 0")
                    elif dv1 <= dv0 and dv1 <= dv2:
                        vehicle2_xy.append((r1[0], r1[1]))
                        print("additional " + str(len(bullet1_xy)) + " fired from vehicle 1")
                    else:
                        vehicle3_xy.append((r2[0], r2[1]))
                        print("additional " + str(len(bullet1_xy)) + " fired from vehicle 2")
                    continue
                else:
                    dv0 = dist(r0, (cX, cY))
                    dv1 = dist((cX, cY),r1)
                    #print(dv1)
                    dv2 = dist(r2, (cX, cY))
                    if dv0 <= dv1 and dv0 <= dv2:
                        min = dv0
                    elif dv1 <= dv0 and dv1 <= dv2:
                        min = dv1
                    else:
                        min = dv2

                    if min <= 10 or min==dv1:
                        if min==dv1 and (cX==567 or r1[0]==(562 or 764 or 763 or 762 or 563 or 564)) and dv1<=31:
                            vehicle2_xy.append((r1[0], r1[1]))
                            bullet1_xy.append((x1, y1))
                            print("additional y vehicle 1 bullets", len(bullet1_xy), str(r1), str((cX, cY)), dv1)
                        elif min==dv0 and min<=15:
                            vehicle1_xy.append((r0[0], r0[1]))
                            bullet1_xy.append((x1, y1))
                            print("additional y vehicle 0 bullets", len(bullet1_xy), str(r0), dv0)
                        elif min == dv2:
                            vehicle3_xy.append((r2[0], r2[1]))
                            bullet1_xy.append((x1, y1))
                            print("additional y vehicle 2 bullets", len(bullet1_xy), str(r2), dv2)
                    continue
                    '''if dv0<=15 and r0[0]+r0[2]-x1<=20:
                        vehicle1_xy.append((r0[0], r0[1]))
                        bullet1_xy.append((x1, y1))
                        print("additional y vehicle 0 bullets", len(bullet1_xy), str(r0), dv0)
                    if dv1<=15 and r1[0]+r1[2]-x1<=20:
                        vehicle2_xy.append((r1[0], r1[1]))
                        bullet1_xy.append((x1, y1))
                        print("additional y vehicle 1 bullets", len(bullet1_xy), str(r1),str((cX,cY)), dv1)
                    if dv2<=10 and r2[0]+r2[2]-x1<=20:
                        vehicle3_xy.append((r2[0], r2[1]))
                        bullet1_xy.append((x1, y1))
                        print("additional y vehicle 2 bullets", len(bullet1_xy),str(r2), dv2)
                    #else:
                        #print("already tracked")
                    continue'''

    image = cv2.resize(frame1, (frame_width,frame_height)) #Resizing the frame to match the output video specification
    out.write(image)    #Writing the frame to output
    cv2.imshow("AoI_Project", frame1) #To show the output
    frame1 = frame2 #Updating of frame1 to next frame
    ret, frame2 = cap.read() #Frame 2 will get the next frame

    if not ret: #Exit reading, if end of Video
        break
    if frame2.shape != (834,952,3):
        break
    if cv2.waitKey(40) == 27:
        break
#Close windows as video ended



print(len(vehicle1_xy),len(vehicle2_xy),len(vehicle3_xy))
cv2.destroyAllWindows()
cap.release()
out.release()

