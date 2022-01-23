import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
# Check which camera to use
cap = cv2.VideoCapture(1)
_, res = cap.read()
res = [res.shape[1], res.shape[0]]
# boundpixel = [res[0]/4, res[1]/4]
boundpixel = 350
print(res)

while True:
    # Read the frame
    _, img = cap.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Border rectangle/based on original resolution
    # cv2.rectangle(img, (int((res[0]/4)), int((res[1]/4))), (int(res[0]/4*3), int(res[1]/4*3)), (255, 0, 0), 3)

    # Border square
    cv2.rectangle(img, (int((res[0]/2)-boundpixel/2), int((res[1]/2)-boundpixel/2)), (int(res[0]/2+boundpixel/2), int(res[1]/2+boundpixel/2)), (0, 255, 0), 3)

    # Detect face
    if len(faces) > 0:

        # Check if face is within boundaries
        if faces[0][0] > int((res[0]/2)-boundpixel/2) and faces[0][0]+faces[0][2] < int(res[0]/2+boundpixel/2) and faces[0][1] > int((res[1]/2)-boundpixel/2) and faces[0][1]+faces[0][3] < int(res[1]/2+boundpixel/2):

            # Draw around face and tag
            cv2.rectangle(img, (faces[0][0], faces[0][1]), (faces[0][0]+faces[0][2], faces[0][1]+faces[0][3]), (255, 0, 0), 1)
            cv2.putText(img, "something cool", (faces[0][0]+faces[0][2], faces[0][1]+faces[0][3]), cv2.FONT_HERSHEY_PLAIN, 0.75, (255,0,0), 1)
            cv2.imwrite("image.jpg", img)


    # Display
    cv2.imshow('facetrack', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()