import cv2
from ultralytics import YOLO
import os
import time
import requests
from dotenv import load_dotenv
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../my-senior-project/Logs/yolo_detection.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
models_path = os.path.join(folder_path, "models")
snapshots_path = os.path.join(folder_path, "Snapshots")

path_Yolo = os.path.join(models_path, "ModelYolo.onnx")
model_Yolo = YOLO(path_Yolo , task="detect")

url_line = "https://notify-api.line.me/api/notify"
TOKEN = os.getenv("API_KEY")
LINE_HEADERS = {"Authorization": "Bearer " + TOKEN}
session = requests.Session()


snake_count = 0
personfall_count = 0
vomit_count = 0

def detect_yolo(frame):
    global snake_count, personfall_count, vomit_count
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
                logging.info("Snake detected in frame")
            elif class_id == 0:
                personfall_found = True
                logging.info("Person fall detected in frame")
            elif class_id == 5:
                vomit_found = True
                logging.info("Vomit detected in frame")
                break
        if snake_found or personfall_found or vomit_found:
            break

    if snake_found:
        snake_count += 1
        logging.debug(f"Snake detection count: {snake_count}")
        if snake_count == 10:
            logging.info("Snake detection threshold reached - sending notification")
            print(f"time Detection : {time.time()}")
            img_snake = os.path.join(snapshots_path, f"snake_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_snake, frame)

            file = {'imageFile': open(img_snake, 'rb')}
            message_S = {'message': 'ตรวจพบสิ่งต้องสงสัยคล้ายงู'}
            response = session.post(url_line, headers=LINE_HEADERS, files=file, data=message_S)
            logging.info(f"Line notification sent for snake detection. Status: {response.status_code}")
            snake_count = 0 
            print(f"time send line : {time.time()}")
    else:
        snake_count = 0

    if personfall_found:
        personfall_count += 1
        logging.debug(f"Person fall detection count: {personfall_count}")
        if personfall_count == 30:
            logging.info("Person fall detection threshold reached - sending notification")
            print(f"time Detection : {time.time()}")
            img_person = os.path.join(snapshots_path, f"personfall_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_person, frame)

            file = {'imageFile': open(img_person, 'rb')}
            message_P = {'message': 'ตรวจพบบุคคลที่คาดว่าต้องการความช่วยเหลือ'}
            response = session.post(url_line, headers=LINE_HEADERS, files=file, data=message_P)
            logging.info(f"Line notification sent for person fall detection. Status: {response.status_code}")
            personfall_count = 0
            print(f"time send line : {time.time()}")
    else:
        personfall_count = 0

    if vomit_found:
        vomit_count += 1
        logging.debug(f"Vomit detection count: {vomit_count}")
        if vomit_count == 3:
            logging.info("Vomit detection threshold reached - sending notification")
            print(f"time Detection : {time.time()}")
            img_vomit = os.path.join(snapshots_path, f"vomit_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_vomit, frame)

            file = {'imageFile': open(img_vomit, 'rb')}
            message_V = {'message': 'ตรวจพบเด็ก / บุคคลที่คาดว่าไม่สามารถช่วยเหลือตัวเองได้'}
            response = session.post(url_line, headers=LINE_HEADERS, files=file, data=message_V)
            logging.info(f"Line notification sent for vomit detection. Status: {response.status_code}")
            vomit_count = 0
            print(f"time send line : {time.time()}")
    else:
        vomit_count = 0

    return results[0].plot()


if __name__ == "__main__":
    logging.info("Starting YOLO detection system")
    video_path = os.path.join(folder_path, "Videos", "Video1.mp4")
    logging.info(f"Using video source: {video_path}")
    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture("rtsp://Rachata:12461246@192.168.0.101:554/stream1")
    # cap = cv2.VideoCapture("http://172.16.11.255:8080/video")
    now = time.time()
    format_time = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Start at : {format_time}")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to read frame from video")
            break  
        
        for _ in range(5):
            cap.grab()
            
        output_frame = detect_yolo(frame)  
        cv2.imshow("YOLO Detection", output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("User requested to stop detection")
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.info("YOLO detection system stopped")

