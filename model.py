import cv2
import numpy

# Initial Haarcascade
face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('model/haarcascade_mcs_mouth.xml')


def detect_face_mask(namefile, file):

    # User Message
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (30, 30)
    weared_mask_font_color = (0, 255, 0)
    not_weared_mask_font_color = (0, 0, 255)
    thickness = 2
    font_scale = 1
    weared_mask = 'Wearing Mask'
    not_weared_mask = 'Not Wearing Mask'
    condition = None

    # Threshold
    bw_threshold = 80

    # Load Image
    # img = cv2.imread(namefile)
    img = cv2.imdecode(numpy.fromstring(
        file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    # Convert img to Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert img to Black and White (Thresholding)
    (thresh, black_and_white) = cv2.threshold(
        gray, bw_threshold, 255, cv2.THRESH_BINARY)

    # Detect Face on Grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Detect Face on Black and White
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)

    if (len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "Face Not Found", org, font, font_scale,
                    weared_mask_font_color, thickness, cv2.LINE_AA)
        condition = "Face Not Found"
    elif (len(faces) == 0 and len(faces_bw) == 1):
        cv2.putText(img, weared_mask, org, font, font_scale,
                    weared_mask_font_color, thickness, cv2.LINE_AA)
        condition = weared_mask
    else:
        # Draw Rectangle on Face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y: y+h, x: x+w]
            roi_color = img[y: y+h, x: x+w]

        # Detect Mouth
        mouth_rects = mouth_cascade.detectMultiScale(roi_gray, 1.3, 5)

        # Face Detected but Mouth not Detected (Wearing Mask)
        if (len(mouth_rects) == 0):
            cv2.putText(img, weared_mask, org, font, font_scale,
                        weared_mask_font_color, thickness, cv2.LINE_AA)
            condition = weared_mask
        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    # Face and Lips are detected but lips coordinates are within face cordinates which `means lips prediction is true and
                    # person is not waring mask
                    cv2.putText(img, not_weared_mask, org, font, font_scale,
                                not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    condition = not_weared_mask
                    # cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    break
    cv2.imwrite(namefile, img)
    return condition