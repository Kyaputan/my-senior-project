import cv2
from ultralytics import YOLO , RTDETR
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
        logging.FileHandler('Logs/main-uiless.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

folder_path = os.path.dirname(os.path.realpath(__file__))
models_path = os.path.join(folder_path, "models")
snapshots_path = os.path.join(folder_path, "Snapshots")

path_Yolo = os.path.join(models_path, "ModelYolo.onnx")
model_Yolo = YOLO(path_Yolo , task="detect")



url_line = "https://notify-api.line.me/api/notify"
TOKEN = os.getenv("API_KEY")
LINE_HEADERS = {"Authorization": "Bearer " + TOKEN}
session = requests.Session()

try:
    message_Start = {'message': 'ยินดีต้อนรับเข้าสู่ ระบบระวังภัยภายในบ้านพร้อมแจ้งเตือนผ่านแอปพลิเคชันไลน์ รูปแบบ UI LESS'}
    START = session.post(url_line, headers=LINE_HEADERS, data=message_Start)
    if START.status_code == 200:
        logging.info(f"Send message success: {START.status_code}")
    else:
        logging.error(f"Error: {START.status_code}")
except Exception as e:
    logging.error(f"Error: {e}")


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
            img_snake = os.path.join(snapshots_path, f"Snake_detected_{int(time.time())}.jpg")
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
            img_person = os.path.join(snapshots_path, f"Personfall_detected_{int(time.time())}.jpg")
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
            img_vomit = os.path.join(snapshots_path, f"Vomit_detected_{int(time.time())}.jpg")
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


            
def Selet_camera():
    while True:
        num = input("เลือกกล้อง (1 = กล้องเว็บแคม, 2 = RTSP, 3 = IP Camera,exit = ออกจากโปรแกรม): ").strip()
        if num == "1":
            logging.info("Selected camera: WebCam")
            return 0
        elif num == "2":
            logging.info("Selected camera: RTSP")
            username = input("กรุณาใส่ Username: ").strip()
            password = input("กรุณาใส่ Password: ").strip()
            ip = input("กรุณาใส่ IP ของกล้อง: ").strip()
            rtsp_url = f"rtsp://{username}:{password}@{ip}:554/stream1"
            logging.info(f"RTSP URL: {rtsp_url}")
            return rtsp_url
        elif num == "3":
            logging.info("Selected camera: IP Camera")
            ip = input("กรุณาใส่ IP ของกล้อง: ").strip()
            port = input("กรุณาใส่ Port ของกล้อง: ").strip()
            url = f"http://{ip}:{port}/video"
            logging.info(f"IP Camera URL: {url}")
            return url
        elif num.lower() == "exit":
            logging.info("Exiting the program...")
            exit()
        else:
            print("กรุณาเลือก 1 หรือ 2 หรือพิมพ์ 'exit' เพื่อออกจากโปรแกรม!")

if __name__ == "__main__":
    cam_source = Selet_camera()
    cap = cv2.VideoCapture(cam_source)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output_frame = detect_yolo(frame)
        cv2.imshow("frame", output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    logging.info("=========================================================================")
