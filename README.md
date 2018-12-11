# Parking-Guiding-LINEbot
We designed a parking guiding LINE bot based on the Heroku cloud platform, which allows users to obtain the real-time parking space information, aiming to satisfy the parking needs of faculty and other people and also help improve the security of parking management.

My LINEbot QR cord

![alt tag](https://i.imgur.com/oY15WFU.png)

Simply click on the “Parking” button on the phone then you can easily enjoy the convenience of obtaining the parking space information. 

![alt tag](https://i.imgur.com/TyemTU1.png)

The parking space imgae is as follow.

![alt tag](https://i.imgur.com/t7K8eYg.jpg)

In addition, it can be further improved by combining with other image processing algorithms to achieve the purpose of identifying license plates and vehicle models. 

# Outline
* [Usage Guide](#usage-guide)
  * [Prerequisites](#prerequisites)
  * [Train the YOLOv3 Program](#train-the-yolov3-program)
  * [Sent the Output Image to LINEbot](#sent-the-output-image-to-lINEbot)
  * [Get the Parking Space Image](#Get-the-parking-space-image)
    * [Prepare Your Own LINE Provider](#prepare-your-own-LINE-provider)
    * [Deploy the LINEbot Program to Heroku](#deploy-the-LINEbot-program-to-heroku)
    * [Set the Webhook URL](#set-the-webhook-url)
* [Other Information](#other-information)
  * [Reference](#Reference)
  * [Contact](#contact)

# Usage Guide
The system is mainly composed of two parts: YOLO real-time object detection program and LINE Bot program.

(1) First, We use 4 cameras to monitor some part of parking space in building 7, Yuan Ze University. Second, in the YOLO program, the result returned by YOLO detection on the camera frame is compared with the original coordinates. Finally, The result is saved as a JPG image
which is sent to LINE bot through the FLASK framework.

(2) In the robot program, the URL of the output image is linked to the Line-bot-sdk. After deploying this program to Heroku cloud platform, we set the webhook URL of our app in LINE Developers. Finally, the LINE bot can communicate with users via the REPLY_MESSAGE and PUSH_MESSAGE functions of the LIEN Messaging API.

## Prerequisites
- [Anaconda](https://www.anaconda.com/download/#linux)

- [OpenCV](https://opencv.org/releases.html)

- [YOLOv3](https://pjreddie.com/darknet/yolo/)

- [YOLO3-4-Py](https://github.com/madhawav/YOLO3-4-Py?fbclid=IwAR2U5mDAT4L195tMx1y3ul9HZ6zyv9lvZDurSMemQxqe1ecQ0VKx_L_DDho)

- [Heroku](https://www.heroku.com/)

Follow the instructions on the YOLO website above to build YOLOv3 and learn how it works. Darknet on the CPU is fast but it's like 500 times faster on GPU! So I strongly suggest you to have an Nvidia GPU and you'll have to install CUDA. 

## Train the YOLOv3 Program
Git clone this repository and run the following command. Output image will be stored in ./YOLO3-4-Py/output
```
cd YOLO3-4-Py
python Parking_1107.py
```
## Sent the Output Image to LINEbot
Before runing sendImg.py, you need to instasll [Flask](http://flask.pocoo.org/docs/1.0/installation/) first.
```
cd YOLO3-4-Py
python sendImg.py
```
## Get the Parking Space Image
### Prepare Your Own LINE Provider
(1) Go to [LINE Developers](https://developers.line.biz/en/) and login with your LINE account to create your own LINE provider.
![alt tag](https://i.imgur.com/nGPF2A1.png)

(2) In the channel setting of your provider, enable webhooks.

(3) Copy and paste the ```Channel access token``` and ```Channel secret``` to the LINEbot code. 
```
Channel_Access_Token = YOUR_CHANNEL_SECRET
Channel_Secret = YOUR_CHANNEL_SECRET
``` 
![alt tag](https://i.imgur.com/vTFEj2L.jpg)

### Deploy the LINEbot Program to Heroku
Please reffer to this tutorial https://github.com/twtrubiks/Deploying-Flask-To-Heroku to learn how to deploy flask to heroku.

The deployed result is shown as follow.

![alt tag](https://i.imgur.com/opCZyum.png)

### Set the Webhook URL
Copy and paste the URL of your app (the URL in the red box of the picture above) to the ```Webhook URL``` in the setting of your LINE provider 

The format of the webhook URL should be like: 
```
https://{your_app_url}/callback
```

# Other Information
## Reference
- [line-bot-tutorial](https://github.com/twtrubiks/line-bot-tutorial/blob/master/README.md)
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- [Running Your Flask Application Over HTTPS](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)


## Contact
For any question, please contact ```Weiwei,Gao: vivisl0607@gmail.com```

Directed by Chiencheng, Lee

Department of Electrical Engineering, Yuan Ze University

135 Yuan-Tung Road, Chung-Li, Taoyuan 320, Taiwan

![alt tag](https://i.imgur.com/cKck6eJ.png)





