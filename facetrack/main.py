import cv2
import time
import math
import base64
from django.test import client
import requests
import socket
print(socket.gethostbyname(socket.gethostname()))

# from smbus2 import SMBus
# from mlx90614 import MLX90614

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the sensor
# sensor = MLX90614(SMBus(1), address=0x5A)

# Check for all accessible camera
arrayCap = 0
limit = 0
cap = cv2.VideoCapture(arrayCap)
while cap.isOpened():
    limit+=1
    cap.release()
    cap = cv2.VideoCapture(limit)
cap.release()

# Reset params to 1st camera
arrayCap = 0
cap = cv2.VideoCapture(arrayCap)

if limit==0:
    print("No camera")

else:
    # Square border size
    borderSize = 300
    
    # capture time in Seconds
    durationCapture = 5
    
    interval = 0;
    while True:
        # Read the frame
        _, img = cap.read()
        
        # Current time
        curTime = time.perf_counter_ns() / 1000000000 

        # Border rectangle/based on original resolution
        # cv2.rectangle(img, (int((res[0]/4)), int((res[1]/4))), (int(res[0]/4*3), int(res[1]/4*3)), (255, 0, 0), 3)

        # Border square
        cv2.rectangle(img, (int((img.shape[1]/2)-borderSize/2), int((img.shape[0]/2)-borderSize/2)), (int(img.shape[1]/2+borderSize/2), int(img.shape[0]/2+borderSize/2)), (0, 255, 0), 3)

        # Detect the faces
        faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)       
        if len(faces) > 0:
            # Check if face is within boundaries
            if faces[0][0] > int((img.shape[1]/2)-borderSize/2) and faces[0][0]+faces[0][2] < int(img.shape[1]/2+borderSize/2) and faces[0][1] > int((img.shape[0]/2)-borderSize/2) and faces[0][1]+faces[0][3] < int(img.shape[0]/2+borderSize/2):
                # Draw border around face and tag

                # temperatureFloat = round(sensor.get_object_1(),2)

                temperatureFloat = 40.0
                tempText = str(temperatureFloat) + " C "

                cv2.rectangle(img, (faces[0][0], faces[0][1]), (faces[0][0]+faces[0][2], faces[0][1]+faces[0][3]), (255, 0, 0), 1)
                cv2.putText(img, tempText, (faces[0][0]+faces[0][2], faces[0][1]+faces[0][3]), cv2.FONT_HERSHEY_PLAIN, 0.75, (0,255,0), 1)
                
                if curTime > interval + durationCapture:
                    
                    imgText = "uploads/img_" + str(math.floor(curTime)) + "_" + str(temperatureFloat) + "C.jpg"
                    
                    # imgText = "uploads/img_" + str(math.floor(curTime)) + ".jpg"
                    
                    cv2.imwrite(imgText, img)
                    interval = curTime + durationCapture
                    if temperatureFloat >= 38:
                        with open(imgText, "rb") as binary_file:
                            binary_file_data = binary_file.read()
                            base64_encoded_data = base64.b64encode(binary_file_data)
                            base64_message = base64_encoded_data.decode('utf-8')

                            # with open('decoded_image.jpg', 'wb') as f:
                            #     decoded_image_data = base64.b64decode(base64_message)
                            #     f.write(decoded_image_data)

                            _url='http://localhost:8000/camera/images/'

                            # payload = {'imageName': imgText,'image':base64_message}
                            payload = {'imageName': imgText,'image':base64_message,'ipAddress':socket.gethostbyname(socket.gethostname()), 'temp': temperatureFloat}
                            # payload = {'imageName': imgText,'image':base64_message,'ipAddress':'127.0.0.1', 'temp': temperatureFloat}
                            r = requests.post(url=_url, data=payload)
                            print(r.text)
                            
        else:
            interval = curTime
        title = 'camera ' + str(arrayCap + 1)
        cv2.imshow(title, img)

        k = cv2.waitKey(30)
        if arrayCap is not (k - 0x30):
            if k>=0x30 and k<(0x30+limit):
                k -= 0x30
                cap.release()
                arrayCap = k
                cap = cv2.VideoCapture(arrayCap)
                cv2.destroyAllWindows()
            if k==27:
                break
    cap.release()
