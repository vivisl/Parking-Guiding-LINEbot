
from pydarknet import Detector, Image
import cv2
import time
import threading
import scipy.misc
import numpy as np
import pathlib
import pickle
# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL, camera):
        self.Frame = []
        self.status = False
        self.isstop = False
        # self.lock = threading.Lock()
        self.url = URL
        
    # 攝影機連接。
        self.capture = cv2.VideoCapture(URL)

    def start(self,n):
        print('ipcam {} started!'.format(n))
        threading.Thread(target=self.queryframe, daemon=True, args=(n,)).start()

    def stop(self,n):
    # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam {} stopped!'.format(n))
   
    def getframe(self):
        #global lock
    # 當有需要影像時，再回傳最新的影像。
        # self.lock.acquire()

        # try:
            # np.copyto(frame, self.Frame)


        # finally:
           # self.lock.release()

        return self.Frame

    def getstatus(self):
    # 當有需要影像時，再回傳最新的影像。
        return self.status
        
    def queryframe(self, cam):
        # global lock
        # self.lock.acquire()
        try:
            while (not self.isstop):
                self.status, self.Frame = self.capture.read()
                if self.status == False:
                    self.capture.release()
                    self.capture = cv2.VideoCapture(self.url)
                    print('restart camera {}... '.format(cam))
                    time.sleep(1)

        finally:
            self.capture.release()
            # self.lock.release()

if __name__ == "__main__":
    # Optional statement to configure preferred GPU. Available only in GPU version.
    # pydarknet.set_cuda_device(0)
    global lock
    
    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    #initialize the path to the cameras 
    URL1 = "rtsp://admin:22065961Kan@140.138.178.23:554/unicast/c1/s1/live"
    URL2 = "rtsp://admin:22065961Kan@140.138.178.23:554/unicast/c2/s1/live"
    URL3 = "rtsp://admin:22065961Kan@140.138.178.23:554/unicast/c3/s1/live"
    URL4 = "rtsp://admin:22065961Kan@140.138.178.23:554/unicast/c4/s1/live"
    # load the cameras 
    
    ipcam1 = ipcamCapture(URL1, 1)
    ipcam2 = ipcamCapture(URL2, 2)
    ipcam3 = ipcamCapture(URL3, 3)
    ipcam4 = ipcamCapture(URL4, 4)


    ipcam1.start(1)
    ipcam2.start(2)
    ipcam3.start(3)
    ipcam4.start(4)
    time.sleep(1)

    fx=0.4
    fy=0.4
    #cap = cv2.VideoCapture("rtsp://admin:22065961Kan@140.138.178.23:554/unicast/c4/s1/live")
    camera_grid_dict = {1:[86, 87, 88, 89], 2:[21, 22], 3:[17,18,19], 4:[12,13,14,15,16]}
    packingSpace=[12,13,14,15,16,17,18,19,21,22,86,87,88,89]
    parktime_fname = 'parktime.bin'
    parttm_path = pathlib.Path(parktime_fname)    

    if parttm_path.is_file():
        print('{} exists'.format(parktime_fname))
        f = open(parktime_fname, 'rb')
        partingtime_dict = pickle.load(f)
        f.close()
    else:
        print('{} does not exist'.format(parktime_fname))
        partingtime_dict = {}
        for i in packingSpace:
            partingtime_dict[i] = None
    # print(partingtime_dict)


    carpath = pathlib.Path('car')
    if not carpath.exists():
        carpath.mkdir() 
        print('no output car path, create one') 


    while True:
        space=[]
        frame1 =ipcam1.getframe()
        frame2 =ipcam2.getframe()    
        frame3 =ipcam3.getframe()            
        frame4 =ipcam4.getframe()
        # np.copyto(frame1, ipcam1.getframe())
        
        numpy_horizontal1=0
        numpy_horizontal2=0

        print('ipcam1 status:', ipcam1.getstatus(), type(frame1))
        if frame1 is not None:
            print('\tshape ', frame1.shape)
            cv2.imwrite('camera1.jpg',frame1)

        print('ipcam2 status:', ipcam2.getstatus(), type(frame2))
        if frame2 is not None:
            print('\tshape ', frame2.shape)
            cv2.imwrite('camera2.jpg',frame2)

        print('ipcam3 status:', ipcam3.getstatus(), type(frame3))
        if frame3 is not None:
            print('\tshape ', frame3.shape)
            cv2.imwrite('camera3.jpg',frame3)

        print('ipcam4 status:', ipcam4.getstatus(), type(frame4))
        if frame4 is not None:
            print('\tshape ', frame4.shape)
            cv2.imwrite('camera4.jpg',frame4)

        tmstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        if ipcam1.getstatus() and type(frame1) is np.ndarray:
            

            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame1)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            print("----------------------------camera 1--------------------------------------------------")            
            print("Elapsed Time for camera 1:",end_time-start_time)
            frontcars=[]
            # (meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h))
            #the detect method return the name,confidence,x-coordinate,y-coordinate,width, and the height of every bounding box
            # representing an object, apply a threshold depending on the distance of a camera to the cars to get the front cars
            for i, obj in enumerate(results):
                print('{}, {}, x{:.2f}, y{:.2f}, w{:.2f}, h{:.2f}'.format(i, 
                	obj[0].decode("utf-8"), obj[2][0],obj[2][1],obj[2][2],obj[2][3]))
                if obj[2][3]>=110 and (obj[0]==b'car' or obj[0]==b'truck'or obj[0]==b'bus' or obj[0]==b'motorbike'):
                    frontcars.append(obj)
                    print('add to frontcars:',i)                    

          #use the x-coordinates to determine which space is not available 
            notavailable=[]

            for i in frontcars:
                x, y, w, h = i[2]
                x1, y1, x2, y2 = int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2)
                car = frame1[y1:y2, x1:x2]
                if x >990:
                    notavailable.append(86)
                    cv2.imwrite('car/c01_86.jpg',car)
                
                if 750 <x < 920:
                    notavailable.append(87)
                    cv2.imwrite('car/c01_87.jpg',car)
            
                if 310 < x < 550:
                    notavailable.append(88)
                    cv2.imwrite('car/c01_88.jpg',car)

                if 120 < x < 310:
                    notavailable.append(89)
                    cv2.imwrite('car/c01_89.jpg',car)

            # get the available spaces
            for i in range(86,90):
                if i not in notavailable:
                    print ("packing space "+str(i)+" is available")
                    space.append(i)

            for i, obj in enumerate(results):
                cat, score, bounds = obj
                x, y, w, h = bounds
                cv2.rectangle(frame1, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,0,255),3)
                strText = '{}-{}'.format(i, str(cat.decode("utf-8")))
                cv2.putText(frame1, strText, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
            
            cv2.imwrite('camera1_out.jpg',frame1)
            w = frame1.shape[1]
            h = frame1.shape[0]
            dsize = (int(fx * w), int(fy * h))
            frame1s = cv2.resize(frame1, dsize)

            #cv2.imshow("preview1", frame1)

        if ipcam2.getstatus() and type(frame2) is np.ndarray:        
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame2)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            print("----------------------------camera 2--------------------------------------------------")
            print("Elapsed Time for camera 2:",end_time-start_time)
            # detect returns (meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h))
            frontcars=[]
            for i, obj in enumerate(results):
                print('{}, {}, x{:.2f}, y{:.2f}, w{:.2f}, h{:.2f}'.format(i, 
                	obj[0].decode("utf-8"), obj[2][0],obj[2][1],obj[2][2],obj[2][3]))
                if obj[2][3]>=170 and (obj[0]==b'car' or obj[0]==b'truck'or obj[0]==b'bus' or obj[0]==b'motorbike'):
                    frontcars.append(obj)
                    print('add to frontcars:',i)


            # print frontcars
            # print(len(frontcars))
                   # if i[]
            notavailable=[]
            for i in frontcars:
                x, y, w, h = i[2]
                x1, y1, x2, y2 = int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2)
                car = frame2[y1:y2, x1:x2]                
                if 700 < x < 930 :
                    notavailable.append(21)
                    cv2.imwrite('car/c02_21.jpg',car)
                
                if 400 <x < 630:
                    notavailable.append(22)
                    cv2.imwrite('car/c02_22.jpg',car)                    
                    
            for i in range(21,23):
                if i not in notavailable:
                    print ("packing space "+str(i)+" is available")
                    space.append(i)    

            for i, obj in enumerate(results):
                cat, score, bounds = obj
                x, y, w, h = bounds
                cv2.rectangle(frame2, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,0,255),3)
                strText = '{}-{}'.format(i, str(cat.decode("utf-8")))
                cv2.putText(frame2, strText, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
            
            cv2.imwrite('camera2_out.jpg',frame2)

            w = frame2.shape[1]
            h = frame2.shape[0]
            dsize = (int(fx * w), int(fy * h))
            frame2s = cv2.resize(frame2, dsize)
            
            #cv2.imshow("preview2", frame2)



        if ipcam3.getstatus() and type(frame3) is np.ndarray:
           
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame3)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            print("----------------------------camera 3--------------------------------------------------")
            print("Elapsed Time for camera 3:",end_time-start_time)
            frontcars=[]
            for i, obj in enumerate(results):
                print('{}, {}, x{:.2f}, y{:.2f}, w{:.2f}, h{:.2f}'.format(i, 
                	obj[0].decode("utf-8"), obj[2][0],obj[2][1],obj[2][2],obj[2][3]))
                if obj[2][3]>=167 and (obj[0]==b'car' or obj[0]==b'truck'or obj[0]==b'bus' or obj[0]==b'motorbike'):
                    frontcars.append(obj)
                    print('add to frontcars:',i)

            # print frontcars
            # print('frontcars:',len(frontcars))
                   # if i[]
            notavailable=[]

            for i in frontcars:
                x, y, w, h = i[2]
                x1, y1, x2, y2 = int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2)
                car = frame3[y1:y2, x1:x2]                
                if 800 < x < 990:
                    notavailable.append(17)
                    cv2.imwrite('car/c03_17.jpg',car)

                if 520 < x < 740:
                    notavailable.append(18)
                    cv2.imwrite('car/c03_18.jpg',car)                    
                
                if 230 < x < 470:
                    notavailable.append(19)
                    cv2.imwrite('car/c03_19.jpg',car)                    
                    
            for i in range(17,20):
                if i not in notavailable:
                    print ("packing space "+str(i)+" is available")
                    space.append(i)

            for i, obj in enumerate(results):
                cat, score, bounds = obj
                x, y, w, h = bounds
                cv2.rectangle(frame3, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,0,255),3)
                strText = '{}-{}'.format(i, str(cat.decode("utf-8")))
                cv2.putText(frame3, strText, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
            
            cv2.imwrite('camera3_out.jpg',frame3)

            w = frame3.shape[1]
            h = frame3.shape[0]
            dsize = (int(fx * w), int(fy * h))
            frame3s = cv2.resize(frame3, dsize)

            #cv2.imshow("preview3", frame3)

        if ipcam4.getstatus() and type(frame4) is np.ndarray:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame4)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            print("----------------------------camera 4--------------------------------------------------")
            print("Elapsed Time for camera 4:",end_time-start_time)

            frontcars=[]
            for i, obj in enumerate(results):
                print('{}, {}, x{:.2f}, y{:.2f}, w{:.2f}, h{:.2f}'.format(i, 
                	obj[0].decode("utf-8"), obj[2][0],obj[2][1],obj[2][2],obj[2][3]))
                if obj[2][3]>=140 and (obj[0]==b'car' or obj[0]==b'truck'or obj[0]==b'bus' or obj[0]==b'motorbike'):
                    frontcars.append(obj)
                    print('add to frontcars:',i)
           
            # print(resu)

            notavailable=[]

            for i in frontcars:
                x, y, w, h = i[2]
                x1, y1, x2, y2 = int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2)
                car = frame4[y1:y2, x1:x2]                
                if  970 < x <1130:
                    notavailable.append(12)
                    cv2.imwrite('car/c04_12.jpg',car)   
                
                if 800 < x <1000:
                    notavailable.append(13)
                    cv2.imwrite('car/c04_13.jpg',car)                    
                
                if 560 < x <800:
                    notavailable.append(14)
                    cv2.imwrite('car/c04_14.jpg',car)                      
                
                if 310 < x <510:
                    notavailable.append(15)
                    cv2.imwrite('car/c04_15.jpg',car)                      
                
                if 120 < x <300:
                    notavailable.append(16)
                    cv2.imwrite('car/c04_16.jpg',car)                      

            for i in range(12,17):
                if i not in notavailable:
                    print ("packing space "+str(i)+" is available")
                    space.append(i)
    

            for i, obj in enumerate(results):
                cat, score, bounds = obj
                x, y, w, h = bounds
                cv2.rectangle(frame4, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,0,255),3)
                strText = '{}-{}'.format(i, str(cat.decode("utf-8")))
                cv2.putText(frame4, strText, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))   
            
            cv2.imwrite('camera4_out.jpg',frame4)

            w = frame4.shape[1]
            h = frame4.shape[0]
            dsize = (int(fx * w), int(fy * h))
            frame4s = cv2.resize(frame4, dsize)
           # cv2.imshow("preview4", frame4)
        



        im_layout = cv2.imread('layout.png')
        im_out = im_layout.copy()
        
        map_dict = {12:(590,172), 13:(590,196),14:(590,220),15:(590,244),16:(590,270),17:(590,302),
            18:(590,323),19:(590,345),21:(590,386),22:(590,408),86:(645,55),87:(612,35),88:(551,55),89:(518,35)}

        available_color = (152, 251, 152)
        not_available_color = (114,128,250)
        tmp_color = (205, 250, 255)
        print('available space:',space)

        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (0,0,0)
      

        for j in packingSpace:
            if j in space:
                cv2.floodFill(im_out, None, map_dict[j], available_color)
                partingtime_dict[j]=None
            else:                
                if partingtime_dict[j]==None:
                    partingtime_dict[j]=time.time()
                    cv2.floodFill(im_out, None, map_dict[j], tmp_color)
                    for ncam in range(1, len(camera_grid_dict)+1):  
                        if j in camera_grid_dict[ncam]:
                            fname = 'car/parktime_grid_{:03d}.jpg'.format(j)
                            if ncam==1:
                                cv2.imwrite(fname,frame1) 
                            elif ncam==2:
                                cv2.imwrite(fname,frame2) 
                            elif ncam==3:
                                cv2.imwrite(fname,frame3) 
                            elif ncam==4:
                                cv2.imwrite(fname,frame4) 

                            break

                else:
                    cv2.floodFill(im_out, None, map_dict[j], not_available_color)
                    park_elapse = int(time.time() - partingtime_dict[j])
                    park_hh = park_elapse//(60*60)
                    park_mm = (park_elapse%3600)//60
                    if j in [86,87,88,89]:
                        x = map_dict[j][0]
                        y = map_dict[j][1]
                        cv2.putText(im_out, '{:d}h'.format(park_hh), (x,y), fontFace, 0.4, font_color)
                        cv2.putText(im_out, '{:d}m'.format(park_mm), (x,y+12), fontFace, 0.4, font_color)
                    else:   
                        park_elapse_str =  '{:d}h{:d}m'.format(park_hh, park_mm)                    
                        cv2.putText(im_out, park_elapse_str, map_dict[j], fontFace, 0.4, font_color)

        cv2.imwrite('./output/parking_space_info.jpg', im_out)
        cv2.putText(im_out, tmstr, (5,im_out.shape[0]-20), fontFace, 1, font_color)
        cv2.imwrite('./output/parking.jpg',im_out)

        # w = im_out.shape[1]
        # h = im_out.shape[0]
        # dsize = (int(fx * w), int(fy * h))
        # im_out = cv2.resize(im_out, dsize)
       # cv2.imshow('cameras', numpy_vertical)
        cv2.imshow('im_out', im_out)

        if type(frame1) is np.ndarray and \
           type(frame2) is np.ndarray and \
           type(frame3) is np.ndarray and \
           type(frame4) is np.ndarray:

            # print('\tshape1 ', frame1.shape, frame1s.shape)
            # print('\tshape2 ', frame2.shape, frame2s.shape)
            # print('\tshape3 ', frame3.shape, frame3s.shape)
            # print('\tshape4 ', frame4.shape, frame4s.shape)

            numpy_horizontal2 = np.hstack((frame1s, frame4s))
            numpy_horizontal1 = np.hstack((frame2s, frame3s))
            numpy_vertical = np.vstack((numpy_horizontal2, numpy_horizontal1))
            cv2.imshow('cameras', numpy_vertical)
            cv2.imwrite('./output/cameras.jpg',numpy_vertical)


        f = open(parktime_fname, 'wb')
        pickle.dump(partingtime_dict, f)
        f.close()

        k = cv2.waitKey(100)
        if k == 0xFF & ord("q"):
            ipcam1.stop(1)
            ipcam2.stop(2)
            ipcam3.stop(3)
            ipcam4.stop(4)
            break

        print('sleeping a few seconds, press ctrl-c to stop...')
        time.sleep(60)
