import numpy as np
import cv2
import dlib
from scipy.spatial import distance as dist
from scipy.spatial import ConvexHull

from imutils import face_utils, rotate_bound
import math


def applyAffineTransform(src, srcTri, dstTri, size):
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT_101)

    return dst


# Check if a point is inside a rectangle
def rectContains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[0] + rect[2]:
        return False
    elif point[1] > rect[1] + rect[3]:
        return False
    return True


# calculate delanauy triangulation
def calculateDelaunayTriangles(rect, points):
    # create subdiv
    subdiv = cv2.Subdiv2D(rect);
    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

    triangleList = subdiv.getTriangleList();

    delaunayTri = []

    pt = []
    for t in triangleList:
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            ind = []
            # Get face-points (from 68 face detector) by coordinates
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if (abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
                        # Three points form a triangle. Triangle array corresponds to the file tri.txt in FaceMorph
            if len(ind) == 3:
                delaunayTri.append((ind[0], ind[1], ind[2]))

        pt = []
    return delaunayTri


def warpTriangle(img1, img2, t1, t2):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    # img2Rect = np.zeros((r2[3], r2[2]), dtype = img1Rect.dtype)

    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)

    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
    (1.0, 1.0, 1.0) - mask)

    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Rect


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

        for i in range(0, len(detectedFaces) - 1, 2):
            faceA = detectedFaces[i]
            faceB = detectedFaces[i + 1]
            # x1 = face.left()
            # y1 = face.top()
            # x2 = face.right()
            # y2 = face.bottom()

            points1 = [(int(p.x), int(p.y)) for p in predictor(frame, faceA).parts()]
            points2 = [(int(p.x), int(p.y)) for p in predictor(frame, faceB).parts()]
            img1 = np.copy(frame)
            img2 = np.copy(frame)
            img1Warped = np.copy(img2)
            hull1 = []
            hull2 = []

            hullIndex = cv2.convexHull(np.array(points2), returnPoints=False)
            for i in range(0, len(hullIndex)):
                hull1.append(points1[int(hullIndex[i])])
                hull2.append(points2[int(hullIndex[i])])

            # Find delanauy traingulation for convex hull points
            sizeImg2 = img2.shape
            rect = (0, 0, sizeImg2[1], sizeImg2[0])
            dt = calculateDelaunayTriangles(rect, hull2)
            if len(dt) == 0:
                quit()
            # Apply affine transformation to Delaunay triangles
            for i in range(0, len(dt)):
                t1 = []
                t2 = []

                # get points for img1, img2 corresponding to the triangles
                for j in range(0, 3):
                    t1.append(hull1[dt[i][j]])
                    t2.append(hull2[dt[i][j]])

                warpTriangle(img1, img1Warped, t1, t2)

            # Calculate Mask
            hull8U = []
            for i in range(0, len(hull2)):
                hull8U.append((hull2[i][0], hull2[i][1]))

            mask = np.zeros(img2.shape, dtype=img2.dtype)

            cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

            r = cv2.boundingRect(np.float32([hull2]))

            center = ((r[0] + int(r[2] / 2), r[1] + int(r[3] / 2)))

            # Clone seamlessly.
            output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

            points1, points2 = points2, points1
            img1 = np.copy(frame)
            img2 = np.copy(frame)
            img1Warped = np.copy(img2)
            hull1 = []
            hull2 = []

            hullIndex = cv2.convexHull(np.array(points2), returnPoints=False)
            for i in range(0, len(hullIndex)):
                hull1.append(points1[int(hullIndex[i])])
                hull2.append(points2[int(hullIndex[i])])

            # Find delanauy traingulation for convex hull points
            sizeImg2 = img2.shape
            rect = (0, 0, sizeImg2[1], sizeImg2[0])
            dt = calculateDelaunayTriangles(rect, hull2)
            if len(dt) == 0:
                quit()
            # Apply affine transformation to Delaunay triangles
            for i in range(0, len(dt)):
                t1 = []
                t2 = []

                # get points for img1, img2 corresponding to the triangles
                for j in range(0, 3):
                    t1.append(hull1[dt[i][j]])
                    t2.append(hull2[dt[i][j]])

                warpTriangle(img1, img1Warped, t1, t2)

            # Calculate Mask
            hull8U = []
            for i in range(0, len(hull2)):
                hull8U.append((hull2[i][0], hull2[i][1]))

            mask = np.zeros(img2.shape, dtype=img2.dtype)

            cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

            r = cv2.boundingRect(np.float32([hull2]))

            center = ((r[0] + int(r[2] / 2), r[1] + int(r[3] / 2)))

            # Clone seamlessly.
            output = cv2.seamlessClone(np.uint8(img1Warped), output, mask, center, cv2.NORMAL_CLONE)


            cv2.imshow("Faces with Filter", output)
        cv2.waitKey(1)


