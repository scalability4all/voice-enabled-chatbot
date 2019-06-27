import numpy as np
import cv2
import dlib
from scipy.spatial import distance as dist
from scipy.spatial import ConvexHull


def EyeSize(eye):
    eyeWidth = dist.euclidean(eye[0], eye[3])
    hull = ConvexHull(eye)
    eyeCenter = np.mean(eye[hull.vertices, :], axis=0)

    eyeCenter = eyeCenter.astype(int)

    return int(eyeWidth), eyeCenter


def PlaceEye(frame, eyeCenter, eyeSize):
    eyeSize = int(eyeSize * 1.5)

    x1 = int(eyeCenter[0, 0] - (eyeSize / 2))
    x2 = int(eyeCenter[0, 0] + (eyeSize / 2))
    y1 = int(eyeCenter[0, 1] - (eyeSize / 2))
    y2 = int(eyeCenter[0, 1] + (eyeSize / 2))

    h, w = frame.shape[:2]

    # check for clipping
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 > w:
        x2 = w
    if y2 > h:
        y2 = h

    #re-calculate the size to avoid clipping
    eyeOverlayWidth = x2 - x1
    eyeOverlayHeight = y2 - y1

    # calculate the masks for the overlay
    eyeOverlay = cv2.resize(filter, (eyeOverlayWidth, eyeOverlayHeight), interpolation=cv2.INTER_AREA)
    mask = cv2.resize(filterMask, (eyeOverlayWidth, eyeOverlayHeight), interpolation=cv2.INTER_AREA)
    mask_inv = cv2.resize(filterMaskInv, (eyeOverlayWidth, eyeOverlayHeight), interpolation=cv2.INTER_AREA)

    # take ROI for the verlay from background, equal to size of the overlay image
    roi = frame[y1:y2, x1:x2]

    # roi_bg contains the original image only where the overlay is not, in the region that is the size of the overlay.
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # roi_fg contains the image pixels of the overlay only where the overlay should be
    roi_fg = cv2.bitwise_and(eyeOverlay, eyeOverlay, mask=mask)

    # join the roi_bg and roi_fg
    dst = cv2.add(roi_bg, roi_fg)

    # place the joined image, saved to dst back over the original image
    frame[y1:y2, x1:x2] = dst


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

filter = cv2.imread('Eye.png',-1)

filterMask = filter[:,:,3]
filterMaskInv = cv2.bitwise_not(filterMask)

filter = filter[:,:,0:3]
origEyeHeight, origEyeWidth = filterMask.shape[:2]

video_capture = cv2.VideoCapture(0)

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((shape.num_parts, 2), dtype=dtype)

	# loop over all facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, shape.num_parts):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords



def add_landmarks(mat, face, frame):
   predictor = dlib.shape_predictor()
   shape = predictor(mat, face)
   shape = shape_to_np(shape)
   for (x, y) in shape:
      cv2.circle(mat, (x, y), 1, (0, 0, 255), -1)


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

            landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, face).parts()])

            leftEye = landmarks[leftEyePoints]
            rightEye = landmarks[rightEyePoints]
            leftEyeSize, leftEyeCenter = EyeSize(leftEye)
            rightEyeSize, rightEyeCenter = EyeSize(rightEye)
            PlaceEye(frame, leftEyeCenter, leftEyeSize)
            PlaceEye(frame, rightEyeCenter, rightEyeSize)

        cv2.imshow("Faces with Filter", frame)
        cv2.waitKey(1)
