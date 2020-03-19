import numpy as np
import cv2
import dlib
from scipy.spatial import distance as dist
from scipy.spatial import ConvexHull

from imutils import face_utils, rotate_bound
import math



def draw_sprite(frame, sprite, x_offset, y_offset):
    (h,w) = (sprite.shape[0], sprite.shape[1])
    (imgH,imgW) = (frame.shape[0], frame.shape[1])

    if y_offset+h >= imgH: #if sprite gets out of image in the bottom
        sprite = sprite[0:imgH-y_offset,:,:]

    if x_offset+w >= imgW: #if sprite gets out of image to the right
        sprite = sprite[:,0:imgW-x_offset,:]

    if x_offset < 0: #if sprite gets out of image to the left
        sprite = sprite[:,abs(x_offset)::,:]
        w = sprite.shape[1]
        x_offset = 0

    #for each RGB chanel
    for c in range(3):
            #chanel 4 is alpha: 255 is not transpartne, 0 is transparent background
            frame[y_offset:y_offset+h, x_offset:x_offset+w, c] =  \
            sprite[:,:,c] * (sprite[:,:,3]/255.0) +  frame[y_offset:y_offset+h, x_offset:x_offset+w, c] * (1.0 - sprite[:,:,3]/255.0)
    return frame

#Adjust the given sprite to the head's width and position
#in case of the sprite not fitting the screen in the top, the sprite should be trimed
def adjust_sprite2head(sprite, head_width, head_ypos, ontop = True):
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    factor = 1.0*head_width/w_sprite
    sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor) # adjust to have the same width as head
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])

    y_orig =  head_ypos-h_sprite if ontop else head_ypos # adjust the position of sprite to end where the head begins
    if (y_orig < 0): #check if the head is not to close to the top of the image and the sprite would not fit in the screen
            sprite = sprite[abs(y_orig)::,:,:] #in that case, we cut the sprite
            y_orig = 0 #the sprite then begins at the top of the image
    return (sprite, y_orig)

# Applies sprite to image detected face's coordinates and adjust it to head
def apply_sprite(image, path2sprite,w,x,y, angle, ontop = True):
    sprite = cv2.imread(path2sprite,-1)
    #print sprite.shape
    sprite = rotate_bound(sprite, angle)
    (sprite, y_final) = adjust_sprite2head(sprite, w, y, ontop)
    image = draw_sprite(image,sprite,x, y_final)

#points are tuples in the form (x,y)
# returns angle between points in degrees
def calculate_inclination(point1, point2):
    x1,x2,y1,y2 = point1[0], point2[0], point1[1], point2[1]
    incl = 180/math.pi*math.atan((float(y2-y1))/(x2-x1))
    return incl


def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:,0])
    y = min(list_coordinates[:,1])
    w = max(list_coordinates[:,0]) - x
    h = max(list_coordinates[:,1]) - y
    return (x,y,w,h)

def get_face_boundbox(points, face_part):
    if face_part == 1:
        (x,y,w,h) = calculate_boundbox(points[17:22]) #left eyebrow
    elif face_part == 2:
        (x,y,w,h) = calculate_boundbox(points[22:27]) #right eyebrow
    elif face_part == 3:
        (x,y,w,h) = calculate_boundbox(points[36:42]) #left eye
    elif face_part == 4:
        (x,y,w,h) = calculate_boundbox(points[42:48]) #right eye
    elif face_part == 5:
        (x,y,w,h) = calculate_boundbox(points[29:36]) #nose
    elif face_part == 6:
        (x,y,w,h) = calculate_boundbox(points[48:68]) #mouth
    return (x,y,w,h)


Path = "shape_predictor_68_face_landmarks.dat"

fullPoints = list(range(0, 68))
facePoints = list(range(17, 68))

jawLinePoints = list(range(0, 17))
rightEyebrowPoints = list(range(17, 22))
leftEyebrowPoints = list(range(22, 27))
nosePoints = list(range(27, 36))
rightEyePoints = list(range(36, 42))
leftEyePoints = list(range(42, 48))
mouthOutlinePoints = list(range(48, 61))
mouthInnerPoints = list(range(61, 68))

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor(Path)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    if ret:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detectedFaces = detector(grayFrame, 0)

        for face in detectedFaces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            landmarks = predictor(frame, face)
            landmarks = face_utils.shape_to_np(landmarks)

            incl = calculate_inclination(landmarks[17], landmarks[26])
            is_mouth_open = (landmarks[66][1] - landmarks[62][1]) >= 15

            (x0, y0, w0, h0) = get_face_boundbox(landmarks, 6)
            (x3, y3, w3, h3) = get_face_boundbox(landmarks, 5)  # nose
            apply_sprite(frame, "doggy_nose.png", w3, x3, y3, incl, ontop=False)

            apply_sprite(frame, "doggy_ears.png", face.width(), x1, y1, incl)

            if is_mouth_open:
                apply_sprite(frame, "doggy_tongue.png", w0, x0, y0, incl, ontop=False)


                #apply_sprite(frame, "doggy_ears.png", w, x, y, incl)

            #if is_mouth_open:
                #apply_sprite(frame, "doggy_tongue.png", w0, x0, y0, incl, ontop=False)
        cv2.imshow("Faces with Filter", frame)
        cv2.waitKey(1)
