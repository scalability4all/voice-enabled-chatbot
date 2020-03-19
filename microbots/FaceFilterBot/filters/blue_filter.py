import numpy as np
import cv2
from collections import Counter
import imutils


def extractSkin(image):
    # Taking a copy of the image
    img =  image.copy()
    # Converting from BGR Colours Space to HSV
    img =  cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  
    # Defining HSV Threadholds
    lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    upper_threshold = np.array([20, 255, 255], dtype=np.uint8)
  
    # Single Channel mask,denoting presence of colours in the specified threshold
    skinMask = cv2.inRange(img,lower_threshold,upper_threshold)
  
    # Cleaning up mask using Gaussian Filter
    skinMask = cv2.GaussianBlur(skinMask,(3,3),0)

    # Extracting skin from the threshold mask
    skin  =  cv2.bitwise_and(img,img,mask=skinMask)
  
    # Converting the image back to BRG color space
    img = cv2.cvtColor(skin,cv2.COLOR_HSV2BGR)

    # Observed BGR to RGBA conversion gives a more appropriate color tint that opencv colormask options
    # Added alpha channel to convert black pixels transparent and overlap (WIP) 
    img_a = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    
    # Return the Skin image
    return img_a


camera = cv2.VideoCapture(0)

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()   
    frame = imutils.resize(frame, width = 500)
    # Call extractSkin() to extract only skin portions of the frame 
    skin = extractSkin(frame)

    b_channel, g_channel, r_channel = cv2.split(frame)

    #creating a dummy alpha channel in frame
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 

    frame_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    # show the skin in the image along with the mask
    cv2.imshow("images", np.hstack([frame_BGRA, skin]))
    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()



