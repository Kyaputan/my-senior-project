import cv2
from ultralytics import YOLO
import os
import time
import requests


folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
models_path = os.path.join(folder_path, "models")
snapshots_path = os.path.join(folder_path, "snapshots")

path_Yolo = os.path.join(models_path, "ModelYolo.onnx")
model_Yolo = YOLO(path_Yolo , task="detect")

url_line = "https://notify-api.line.me/api/notify"
TOKEN = "TOKEN_LINE_API"
LINE_HEADERS = {"Authorization": "Bearer " + TOKEN}
session = requests.Session()


snake_count = 0
personfall_count = 0
vomit_count = 0

def detect_yolo(frame):
    global snake_count, personfall_count, vomit_count  # ใช้ global เพื่อให้ค่าถูกเก็บไว้
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    results = model_Yolo.predict(frame, conf=0.2, iou=0.45)

    snake_found = False
    personfall_found = False
    vomit_found = False

    for result in results:
        for detection in result.boxes:
            class_id = int(detection.cls)
            if class_id == 3:
                snake_found = True
            elif class_id == 0:
                personfall_found = True
            elif class_id == 5:
                vomit_found = True
                break
        if snake_found or personfall_found or vomit_found:
            break

    if snake_found:
        snake_count += 1
        if snake_count == 10:
            img_snake = os.path.join(snapshots_path, f"snake_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_snake, frame)

            file = {'imageFile': open(img_snake, 'rb')}
            message_S = {'message': 'ตรวจพบสิ่งต้องสงสัยคล้ายงู'}
            session.post(url_line, headers=LINE_HEADERS, files=file, data=message_S)
            snake_count = 0 
    else:
        snake_count = 0

    if personfall_found:
        personfall_count += 1
        if personfall_count == 30:
            img_person = os.path.join(snapshots_path, f"personfall_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_person, frame)

            file = {'imageFile': open(img_person, 'rb')}
            message_P = {'message': 'ตรวจพบบุคคลที่คาดว่าต้องการความช่วยเหลือ'}
            session.post(url_line, headers=LINE_HEADERS, files=file, data=message_P)
            personfall_count = 0
    else:
        personfall_count = 0

    if vomit_found:
        vomit_count += 1
        if vomit_count == 3:
            img_vomit = os.path.join(snapshots_path, f"vomit_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_vomit, frame)

            file = {'imageFile': open(img_vomit, 'rb')}
            message_V = {'message': 'ตรวจพบเด็ก / บุคคลที่คาดว่าไม่สามารถช่วยเหลือตัวเองได้'}
            session.post(url_line, headers=LINE_HEADERS, files=file, data=message_V)
            vomit_count = 0
    else:
        vomit_count = 0

    return results[0].plot()


if __name__ == "__main__":
    video_path = os.path.join(folder_path, "Videos", "Video1.mp4")
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  
        output_frame = detect_yolo(frame)  
        cv2.imshow("YOLO Detection", output_frame)

   
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
