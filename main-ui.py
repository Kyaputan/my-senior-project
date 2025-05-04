try:
    import customtkinter as ctk
    import cv2
    from PIL import Image, ImageTk
    from ultralytics import YOLO , RTDETR
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import os
    import time
    import threading
    import face_recognition
    import requests
    from queue import Queue
    import numpy as np
    from dotenv import load_dotenv
    import logging
except Exception as e:
    print(f"An error occurred: {e}")

logging.basicConfig(
    filename="Logs/main.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8", 
)

load_dotenv()
API_KEY = os.getenv("API_KEY")
global_selected_quality = ""
ip_camera_url_1 = ip_camera_url_2 = ip_camera_url_3 = ip_camera_url_4 = ip_camera_url_5 = ip_camera_url_6 = ""
url_1 = url_2 = url_3 = url_4 = url_5 = url_6 = ""

session = requests.Session()
root = ctk.CTk()
folder_path = os.path.dirname(os.path.realpath(__file__))
path_Yolo = os.path.join(folder_path, "models", "ModelYolo.onnx")
path_RTDETR = os.path.join(folder_path, "models", "ModelRT.pt")

Send_message = False


def send_message(message, image_path=None):
    if Send_message:
        try:
            url_line = "https://notify-api.line.me/api/notify"
            LINE_HEADERS = {"Authorization":"Bearer "+ API_KEY}
            response = session.post(url_line, headers=LINE_HEADERS , data = {'message': "status_code : 200"})
            try:    
                if image_path:
                    with open(image_path, 'rb') as file:
                        files = {'imageFile': file}
                        message_data = {'message': message}
                        time.sleep(0.3)  
                        response = session.post(url_line, headers=LINE_HEADERS, files=files, data=message_data)
                        if response.status_code == 200:
                            logging.info(f"Successfully sent message and image: {response.status_code}")
                        else:
                            logging.error(f"Failed to send message and image: {response.status_code}")
                else:
                    message_data = {'message': message}
                    response = session.post(url_line, headers=LINE_HEADERS, data=message_data)
                    if response.status_code == 200:
                        logging.info(f"Successfully sent message: {response.status_code}")
                    else:
                        logging.error(f"Failed to send message: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    else:
        logging.info("Closing message sending")


try:
    model_Yolo = YOLO(path_Yolo, task="detect")
    model_RTDETR = YOLO(path_RTDETR)

    logging.info("Successfully loaded YOLO and RTDETR models")  
except Exception as e:
    logging.error(f"An error occurred in loading the model: {e}") 

global selected_value, cap_a, cap_b, cap_r , detection_mode, cap_c , cap_d , cap_e , cap_f , cap_g
snake_count = personfall_count = vomit_count = 0
running_a = running_b = running_r = running_c = running_d = running_e = running_f = running_g = False
known_face_images = []
known_face_encodings = []
known_face_names = []
All_name = []
last_known_notified_time = last_unknown_notified_time = 0
unknown_frame_count = known_frame_count = 0
lock = threading.Lock()
frame_counter_b =active_frame_count_b = 0
frame_counter_c =active_frame_count_c = 0
frame_counter_d =active_frame_count_d = 0
frame_counter_e =active_frame_count_e = 0
frame_counter_f =active_frame_count_f = 0
frame_counter_g =active_frame_count_g = 0
interval = 5
Face_path = os.path.join(folder_path, "database")
image_count  = 0
home_frame = second_frame = Third_frame = None
entry_name = entry_password_sitting = url_now = ""
images_logos = {}
Additional = None

def load_image():
    global images_logos
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
    images_logos["logo_BG_image"] = ctk.CTkImage(
        Image.open(os.path.join(image_path, "bg_gradient.jpg")), size=(1080, 1080)
    )
    images_logos["small_logo_KMITL_image"] = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(76, 76)
    )
    images_logos["logo_KMITL_image"] = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(130, 130)
    )
    images_logos["logo_RIE_image"] = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(130, 130)
    )
    images_logos["address_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "address-book for light.png")),
        dark_image=Image.open(os.path.join(image_path, "address-book for dark.png")),
        size=(20, 20),
    )
    images_logos["camera_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "camera for light.png")),
        dark_image=Image.open(os.path.join(image_path, "camera for dark.png")),
        size=(20, 20),
    )
    images_logos["home_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "home for light.png")),
        dark_image=Image.open(os.path.join(image_path, "home for dark.png")),
        size=(20, 20),
    )
    images_logos["lock_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "lock for light.png")),
        dark_image=Image.open(os.path.join(image_path, "lock for dark.png")),
        size=(20, 20),
    )
    images_logos["sitting_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "settings for light.png")),
        dark_image=Image.open(os.path.join(image_path, "settings for dark.png")),
        size=(20, 20),
    )
    images_logos["trash_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "trash for light.png")),
        dark_image=Image.open(os.path.join(image_path, "trash for dark.png")),
        size=(20, 20),
    )
    images_logos["user_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "user for light.png")),
        dark_image=Image.open(os.path.join(image_path, "user for dark.png")),
        size=(20, 20),
    )
    images_logos["video_logo"] = ctk.CTkImage(
        light_image=Image.open(
            os.path.join(image_path, "video-camera-alt for light.png")
        ),
        dark_image=Image.open(
            os.path.join(image_path, "video-camera-alt for dark.png")
        ),
        size=(20, 20),
    )
    images_logos["mode_event_icon"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "contrast.png")),
        dark_image=Image.open(os.path.join(image_path, "moon-phase.png")),
        size=(30, 30),
    )
    images_logos["IP_address_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "ip-address for light.png")),
        dark_image=Image.open(os.path.join(image_path, "ip-address for dark.png")),
        size=(20, 20),
    )
    images_logos["rescue_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "rescue for light.png")),
        dark_image=Image.open(os.path.join(image_path, "rescue for dark.png")),
        size=(30, 30),
    )
    images_logos["baby_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "baby for light.png")),
        dark_image=Image.open(os.path.join(image_path, "baby for dark.png")),
        size=(30, 30),
    )
    images_logos["snake_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "snake for light.png")),
        dark_image=Image.open(os.path.join(image_path, "snake for dark.png")),
        size=(30, 30),
    )
    images_logos["bandit_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "bandit for light.png")),
        dark_image=Image.open(os.path.join(image_path, "bandit for dark.png")),
        size=(30, 30),
    )
    images_logos["loupe_logo"] = ctk.CTkImage(
        light_image=Image.open(os.path.join(image_path, "loupe.png")), size=(30, 30)
    )

send_message(
    message="Welcome to the My-SENIOR-PROJECT",
    image_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "KMITL-Photoroom.png")
)


def quality_selected(selected_port):
    global global_selected_quality
    global_selected_quality = selected_port

    if selected_port == "Select Quality":
        print("Selected quality: No quality selected")
        global_selected_quality = "stream2"
    elif selected_port == "High Quality":
        print("Selected quality: stream1")
        global_selected_quality = "stream1"
    elif selected_port == "High Performance":
        print("Selected quality: stream2")
        global_selected_quality = "stream2"


def show_frame(frame_name):
    global home_frame, second_frame, Third_frame
    home_frame.pack_forget()
    second_frame.pack_forget()
    Third_frame.pack_forget()

    if frame_name == "home":
        home_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    elif frame_name == "frame_2":
        second_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    elif frame_name == "frame_3":
        Third_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)


def find_known_face_names():
    global image_count
    folder_path = os.path.dirname(os.path.realpath(__file__))
    Face_path = os.path.join(folder_path, "Database")

    for filename in os.listdir(Face_path):
        image_count += 1
        if filename.endswith(".jpg"):
            image_path = os.path.join(Face_path, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            time.sleep(0.3)

            if len(encoding) > 0:
                encoding_exists = False
                for known_encoding in known_face_encodings:
                    distance = np.linalg.norm(known_encoding - encoding[0])
                    if distance < 0.6:
                        encoding_exists = True
                        break

                if not encoding_exists:
                    known_face_images.append(image)
                    known_face_encodings.append(encoding[0])
                    name = os.path.splitext(filename)[0]
                    known_face_names.append(name)
                    time.sleep(0.1)

    if len(known_face_names) == 0:   
        messagebox.showerror("Error", "No Face input received")
        logging.error("No face input received")
    else:
        print(f"Known people count: {len(known_face_names)}")
        logging.info(f"Known people count: {len(known_face_names)}")
    print(f"Number of images in the folder: {image_count} images")


def show_frame_r(label_r, folder_path, interval=5):
    global running_r, cap_r, image_count, start_time
    if not running_r:
        return

    if not cap_r.isOpened():
        print("Failed to open camera")
        return

    ret, frame = cap_r.read()
    if not ret:
        print("Failed to grab frame")
        return
    start_time = time.time()
    small_frame = cv2.resize(frame, (320, 240))
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    detect_bounding_box(small_frame)

    img = Image.fromarray(small_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    label_r.imgtk = imgtk
    label_r.configure(image=imgtk)
    label_r.after(70, show_frame_r, label_r, folder_path, interval)


def toggle_camera_r():
    global running_r, cap_r, interval
    if running_r:
        running_r = False
        cap_r.release()
    else:
        running_r = True
        cap_r = cv2.VideoCapture(0)  
        folder_path = os.path.dirname(os.path.realpath(__file__))
        Face_path = os.path.join(folder_path, "database")
        thread_r = threading.Thread(
            target=show_frame_r, args=(label_r, Face_path, interval)
        )
        thread_r.start()


def detect_yolo(frame):
    global snake_count, personfall_count, vomit_count
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
        print(f"snake_count : {snake_count}")
        if snake_count == 10:
            
            img_folder = os.path.join(folder_path, "Snapshots")
            img_snake = os.path.join(img_folder, f"Snake_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_snake, frame)
            message_S = 'Detected snake'
            send_message(message_S, image_path=img_snake)
            snake_count = 0
    else:
        snake_count = 0

    if personfall_found:
        personfall_count += 1
        print(f"personfall_count : {personfall_count}")
        if personfall_count == 30: 
            
            img_folder = os.path.join(folder_path, "Snapshots")
            img_person = os.path.join(img_folder, f"Personfall_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_person, frame)
            message_P = 'Detected child / person who may need help'
            send_message(message_P, image_path=img_person)
            personfall_count = 0 
    else:
        personfall_count = 0 

    if vomit_found:
        vomit_count += 1
        print(f"vomit_count : {vomit_count}")
        if vomit_count == 3: 
            
            img_folder = os.path.join(folder_path, "Snapshots")
            img_vomit = os.path.join(img_folder, f"Vomit_detected_{int(time.time())}.jpg")
            cv2.imwrite(img_vomit, frame)
            message_V = 'Detected child / person who may need help'
            send_message(message_V, image_path=img_vomit)
            vomit_count = 0   
    else:
        vomit_count = 0 
    return results[0].plot()


def face_recog(frame):
    global last_known_notified_time, last_unknown_notified_time, face_encodings
    global unknown_frame_count, known_frame_count, known_face_names, face_locations
    face_names = []
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding
        )
        best_match_index = face_distances.argmin()
        
        confidence = (1 - face_distances[best_match_index]) * 100  
        
        if matches[best_match_index] and confidence > 45:
            name = known_face_names[best_match_index]
        face_names.append(name)
        current_time = time.time()

        if name == "Unknown":
            unknown_frame_count += 1
            if unknown_frame_count >= 5:
                known_frame_count = 0
            print("test_face_unknown")
            print(f"unknown_frame_count = {unknown_frame_count}")
            if unknown_frame_count >= 10:
                if current_time - last_unknown_notified_time > 20:
                    img_folder = os.path.join(folder_path, "Snapshots")
                    img_unknow = os.path.join(img_folder, f"Unknow_{int(time.time())}.jpg")
                    frame_rgb = frame[:, :, ::-1]
                    cv2.imwrite(img_unknow, frame_rgb)
                    message_b = "Detected unknown person"
                    send_message(message_b, image_path=img_unknow)
                    unknown_frame_count = 0
                    last_unknown_notified_time = current_time
        else:
            known_frame_count += 1 

            if known_frame_count >= 5:
                unknown_frame_count = 0
            print("test_face_known")
            print(f"known_frame_count = {known_frame_count}")
            if known_frame_count >= 10:
                if current_time - last_known_notified_time > 10:
                    
                    img_folder = os.path.join(folder_path, "Snapshots")
                    img_know = os.path.join(img_folder, f"Known_{name}_{int(time.time())}.jpg")
                    frame_rgb = frame[:, :, ::-1]
                    cv2.imwrite(img_know, frame_rgb)
                    message_r = f"Detected {name}"
                    send_message(message_r, image_path=img_know)
                    known_frame_count = 0
                    last_known_notified_time = current_time
    return frame


def show_frame_a(label_a, detection_mode):
    global running_a, cap_a
    if running_a:
        if not cap_a.isOpened():
            print("Failed to open camera")
            return
        ret, frame = cap_a.read()
        if not ret:
            print("Failed to grab frame")
            return
        small_frame = cv2.resize(frame, (320, 320))
        small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        mode = detection_mode.get()
        if mode == "Face-Detection-Mode":
            recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
            recognition_thread.start()
        elif mode == "Danger-Scan-Mode":
            small_frame = detect_yolo(small_frame)
        elif mode == "Full-Protection-Mode":
            small_frame = detect_yolo(small_frame)
            small_frame = face_recog(small_frame)
        img = Image.fromarray(small_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label_a.imgtk = imgtk
        label_a.configure(image=imgtk)
        label_a.after(70, show_frame_a, label_a, detection_mode)


def show_frame_b(label_b, detection_mode, url_1):
    global running_b, cap_b, frame_counter_b, active_frame_count_b
    if url_1:
        if running_b:
            if not cap_b.isOpened():
                print("Failed to open camera")
                return

            for _ in range(5):
                cap_b.grab()

            ret, frame = cap_b.read()
            if not ret:
                print("Failed to grab frame")
                return
            small_frame = cv2.resize(frame, (320, 320))
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            if active_frame_count_b < 30:
                mode = detection_mode.get()
                if mode == "Face_Recognition":
                    recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                    recognition_thread.start()
                elif mode == "Danger-Scan-Mode":
                    small_frame = detect_yolo(small_frame)
                elif mode == "Full-Protection-Mode":
                    small_frame = detect_yolo(small_frame)
                    small_frame = face_recog(small_frame)
                active_frame_count_b += 1
            elif frame_counter_b < 10:
                frame_counter_b += 1
            else:
                active_frame_count_b = 0
                frame_counter_b = 0
            img = Image.fromarray(small_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_b.imgtk = imgtk
            label_b.configure(image=imgtk)
            label_b.after(200, show_frame_b, label_b, detection_mode, url_1)
    else:
        messagebox.showerror("Error", "No address input received")


def toggle_camera_a():
    global running_a, cap_a
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first.")
        logging.error("No face input received")
        return
    if running_a:
        running_a = False
        cap_a.release()
    else:
        running_a = True
        cap_a = cv2.VideoCapture(0)
        thread_a = threading.Thread(target=show_frame_a, args=(label_a, detection_mode))
        thread_a.start()


def toggle_camera_b():
    global running_b, cap_b, url_1
    if not url_1:
        messagebox.showerror("Error", "No address input received")
        return
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first."
        )
        logging.error("No face input received")
        return
    if running_b:
        running_b = False
        cap_b.release()
    else:
        print("url_1", url_1)
        running_b = True
        cap_b = cv2.VideoCapture(url_1)
        thread_b = threading.Thread(
            target=show_frame_b, args=(label_b, detection_mode, url_1)
        )
        thread_b.start()

def show_frame_c(label_c, detection_mode, url_2):
    global running_c, cap_c, frame_counter_c , active_frame_count_c
    if url_2:
        if running_c:
            if not cap_c.isOpened():
                print("Failed to open camera")
                return

            for _ in range(5):
                cap_c.grab()

            ret, frame = cap_c.read()
            if not ret:
                print("Failed to grab frame")
                return
            small_frame = cv2.resize(frame, (320, 320))
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            if active_frame_count_c < 30:
                mode = detection_mode.get()
                if mode == "Face-Detection-Mode":
                    recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                    recognition_thread.start()
                elif mode == "Danger-Scan-Mode":
                    small_frame = detect_yolo(small_frame)
                elif mode == "Full-Protection-Mode":
                    small_frame = detect_yolo(small_frame)
                    small_frame = face_recog(small_frame)
                active_frame_count_c += 1
            elif frame_counter_c  < 10:
                frame_counter_c  += 1
            else:
                active_frame_count_c = 0
                frame_counter_c  = 0
            img = Image.fromarray(small_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_c.imgtk = imgtk
            label_c.configure(image=imgtk)
            label_c.after(200, show_frame_c, label_c, detection_mode, url_2)
    else:
        messagebox.showerror("Error", "No address input received")

def toggle_camera_c():
    global running_c, cap_c, url_2
    if not url_2:
        messagebox.showerror("Error", "No address input received")
        return
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first."
        )
        return
    if running_c:
        running_c = False
        cap_c.release()
    else:
        print("url_2", url_2)
        running_c = True
        cap_c = cv2.VideoCapture(url_2)
        thread_c = threading.Thread(
            target=show_frame_c, args=(label_c, detection_mode, url_2)
        )
        thread_c.start()

def show_frame_d(label_d, detection_mode, url_3):
    global running_d, cap_d, frame_counter_d, active_frame_count_d
    if url_3:
        if running_d:
            if not cap_d.isOpened():
                print("Failed to open camera")
                return

            for _ in range(5):
                cap_d.grab()

            ret, frame = cap_d.read()
            if not ret:
                print("Failed to grab frame")
                return
            small_frame = cv2.resize(frame, (320, 320))
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            if active_frame_count_d < 30:
                mode = detection_mode.get()
                if mode == "Face_Recognition":
                    recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                    recognition_thread.start()
                elif mode == "Danger-Scan-Mode":
                    small_frame = detect_yolo(small_frame)
                elif mode == "Full-Protection-Mode":
                    small_frame = detect_yolo(small_frame)
                    small_frame = face_recog(small_frame)
                active_frame_count_d += 1
            elif frame_counter_d < 10:
                frame_counter_d += 1
            else:
                active_frame_count_d = 0
                frame_counter_d = 0
            img = Image.fromarray(small_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_d.imgtk = imgtk
            label_d.configure(image=imgtk)
            label_d.after(200, show_frame_d, label_d, detection_mode, url_3)
    else:
        messagebox.showerror("Error", "No address input received")

def toggle_camera_d():
    global running_d, cap_d, url_3
    if not url_3:
        messagebox.showerror("Error", "No address input received")
        return
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first."
        )
        return
    if running_d:
        running_d = False
        cap_d.release()
    else:
        print("url_3", url_3)
        running_d = True
        cap_d = cv2.VideoCapture(url_3)
        thread_d = threading.Thread(
            target=show_frame_d, args=(label_d, detection_mode, url_3)
        )
        thread_d.start()

def show_frame_e(label_e, detection_mode, url_4):
    global running_e, cap_e, frame_counter_e, active_frame_count_e
    if url_4:
        if running_e:
            if not cap_e.isOpened():
                print("Failed to open camera")
                return

            for _ in range(5):
                cap_e.grab()

            ret, frame = cap_e.read()
            if not ret:
                print("Failed to grab frame")
                return
            small_frame = cv2.resize(frame, (320, 320))
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            if active_frame_count_e < 30:
                mode = detection_mode.get()
                if mode == "Face-Detection-Mode":
                    recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                    recognition_thread.start()
                elif mode == "Danger-Scan-Mode":
                    small_frame = detect_yolo(small_frame)
                elif mode == "Full-Protection-Mode":
                    small_frame = detect_yolo(small_frame)
                    small_frame = face_recog(small_frame)
                active_frame_count_e += 1
            elif frame_counter_e < 10:
                frame_counter_e += 1
            else:
                active_frame_count_e = 0
                frame_counter_e = 0
            img = Image.fromarray(small_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_e.imgtk = imgtk
            label_e.configure(image=imgtk)
            label_e.after(200, show_frame_e, label_e, detection_mode, url_4)
    else:
        messagebox.showerror("Error", "No address input received")

def toggle_camera_e():
    global running_e, cap_e, url_4
    if not url_4:
        messagebox.showerror("Error", "No address input received")
        return
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first."
        )
        return
    if running_e:
        running_e = False
        cap_e.release()
    else:
        print("url_4", url_4)
        running_e = True
        cap_e = cv2.VideoCapture(url_4)
        thread_e = threading.Thread(
            target=show_frame_e, args=(label_e, detection_mode, url_4)
        )
        thread_e.start()

def show_frame_f(label_f, detection_mode, url_5):
    global running_f, cap_f, frame_counter_f, active_frame_count_f
    if url_5:
        if running_f:
            if not cap_f.isOpened():
                print("Failed to open camera")
                return

            for _ in range(5):
                cap_f.grab()

            ret, frame = cap_f.read()
            if not ret:
                print("Failed to grab frame")
                return
            small_frame = cv2.resize(frame, (320, 320))
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            if active_frame_count_f < 30:
                mode = detection_mode.get()
                if mode == "Face-Detection-Mode":
                    recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                    recognition_thread.start()
                elif mode == "Danger-Scan-Mode":
                    small_frame = detect_yolo(small_frame)
                elif mode == "Full-Protection-Mode":
                    small_frame = detect_yolo(small_frame)
                    small_frame = face_recog(small_frame)
                active_frame_count_f += 1
            elif frame_counter_f < 10:
                frame_counter_f += 1
            else:
                active_frame_count_f = 0
                frame_counter_f = 0
            img = Image.fromarray(small_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_f.imgtk = imgtk
            label_f.configure(image=imgtk)
            label_f.after(200, show_frame_f, label_f, detection_mode, url_5)
    else:
        messagebox.showerror("Error", "No address input received")

def toggle_camera_f():
    global running_f, cap_f, url_5
    if not url_5:
        messagebox.showerror("Error", "No address input received")
        return
    if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
        messagebox.showerror(
            "Error", "No known faces available. Please add known faces first."
        )
        return
    if running_f:
        running_f = False
        cap_f.release()
    else:
        print("url_5", url_5)
        running_f = True
        cap_f = cv2.VideoCapture(url_5)
        thread_f = threading.Thread(
            target=show_frame_f, args=(label_f, detection_mode, url_5)
        )
        thread_f.start()


def show_frame_g(label_g, detection_mode, url_6):
            global running_g, cap_g, frame_counter_g, active_frame_count_g
            if url_6:
                if running_g:
                    if not cap_g.isOpened():
                        print("Failed to open camera")
                        return

                    for _ in range(5):
                        cap_g.grab()

                    ret, frame = cap_g.read()
                    if not ret:
                        print("Failed to grab frame")
                        return
                    small_frame = cv2.resize(frame, (320, 320))
                    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                    
                    if active_frame_count_g < 30:
                        mode = detection_mode.get()
                        if mode == "Face-Detection-Mode":
                            recognition_thread = threading.Thread(target=face_recog, args=(small_frame,))
                            recognition_thread.start()
                        elif mode == "Danger-Scan-Mode":
                            small_frame = detect_yolo(small_frame)
                        elif mode == "Full-Protection-Mode":
                            small_frame = detect_yolo(small_frame)
                            small_frame = face_recog(small_frame)
                        active_frame_count_g += 1
                    elif frame_counter_g < 10:
                        frame_counter_g += 1
                    else:
                        active_frame_count_g = 0
                        frame_counter_g = 0
                    img = Image.fromarray(small_frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    label_g.imgtk = imgtk
                    label_g.configure(image=imgtk)
                    label_g.after(200, show_frame_g, label_g, detection_mode, url_6)
            else:
                messagebox.showerror("Error", "No address input received")

def toggle_camera_g():
            global running_g, cap_g, url_6
            if not url_6:
                messagebox.showerror("Error", "No address input received")
                return
            if detection_mode.get() == "Face_Recognition" and len(known_face_names) == 0:
                messagebox.showerror(
                    "Error", "No known faces available. Please add known faces first."
                )
                return
            if running_g:
                running_g = False
                cap_g.release()
            else:
                print("url_6", url_6)
                running_g = True
                cap_g = cv2.VideoCapture(url_6)
                thread_g = threading.Thread(
                    target=show_frame_g, args=(label_g, detection_mode, url_6)
                )
                thread_g.start()



def start():
    global Start_window, label_a, label_b, detection_mode 
    find_known_face_names()
    Start_window = ctk.CTkToplevel(root)
    Start_window.title("Main Detection")
    screen_width = Start_window.winfo_screenwidth() / 2
    screen_height = Start_window.winfo_screenheight() / 2
    Start_window.geometry(f"{screen_width}x{screen_height}")
    Start_window.resizable(False, False)
    load_image()
 
    bg_image_label = ctk.CTkLabel(
        Start_window, text="", image=images_logos["logo_BG_image"]
    )
    bg_image_label.place(
        relx=0, rely=0, relwidth=1, relheight=1
    )
    bg_image_label.lower()


    logo_frame = ctk.CTkFrame(Start_window)
    logo_frame.pack(
        fill="x", pady=(0, 10)
    )  

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=images_logos["logo_KMITL_image"],
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame,
        text="",
        image=images_logos["logo_RIE_image"],
        fg_color="white",
        corner_radius=20,
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=12, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))


    video_frame = ctk.CTkFrame(Start_window)
    video_frame.pack(fill="y", pady=5) 

    frame_a = ctk.CTkFrame(
        video_frame, width=320, height=320, fg_color="white", corner_radius=20
    )
    frame_a.pack(side="left", expand=True, anchor="n", pady=(5, 10), padx=(30, 100))
    label_a = ctk.CTkLabel(
        frame_a, text="", image=images_logos["logo_KMITL_image"], width=320, height=320
    )
    label_a.pack(side="top", expand=True, padx=10)  
    toggle_a_button = ctk.CTkButton(
        frame_a,
        text="Camera 1",
        command=toggle_camera_a,
        fg_color="#1F6AA5",
        hover_color="#154870",
    )
    toggle_a_button.pack()

    frame_b = ctk.CTkFrame(
        video_frame, width=320, height=320, fg_color="white", corner_radius=20
    )
    frame_b.pack(side="right", expand=True, anchor="n", pady=(5, 10), padx=(100, 30))
    label_b = ctk.CTkLabel(
        frame_b, text="", image=images_logos["logo_KMITL_image"], width=320, height=320
    )
    label_b.pack(
        side="top", expand=True, padx=10
    ) 
    toggle_b_button = ctk.CTkButton(
        frame_b,
        text="Camera 2",
        command=toggle_camera_b,
        fg_color="#1F6AA5",
        hover_color="#154870",
    )
    toggle_b_button.pack()
    
    menu_frame = ctk.CTkFrame(Start_window, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)
    
    button1 = ctk.CTkButton(
        menu_frame,
        text="Back",
        corner_radius=8,
        command=close_window,
        width=100,
        fg_color="#E74C3C",
        hover_color="#C0392B",
    )
    button1.pack(side="left", padx=10, pady=10)
    
    button2 = ctk.CTkButton(
        menu_frame,
        text="Setting",
        corner_radius=8,
        command=go_sitting,
        width=100,
        fg_color="#2ECC71",
        hover_color="#27AE60",
    )
    button2.pack(side="left", padx=10, pady=10)

    button3 = ctk.CTkButton(
        menu_frame,
        text="Face Recognition",
        corner_radius=8,
        command=go_Face_Recognition,
        width=120,
        fg_color="#3498DB",
        hover_color="#2980B9",
    )
    button3.pack(side="left", padx=10, pady=10)
    
    
    button4 = ctk.CTkButton(
        menu_frame,
        text="Add Camera",
        corner_radius=8,
        command=Additional_Detection_1,
        width=120,
        fg_color="#3498DB",
        hover_color="#2980B9",
    )
    button4.pack(side="left", padx=10, pady=10)



    detection_mode_frame = ctk.CTkFrame(Start_window, corner_radius=8)
    detection_mode_frame.pack(pady=5, padx=10, fill="x")

    # Compact header
    detection_mode_label = ctk.CTkLabel(
        detection_mode_frame,
        text="Detection Mode",
        font=ctk.CTkFont(size=16, weight="bold"),
        anchor="center"
    )
    detection_mode_label.pack(pady=5, fill="x")

    # Compact modes frame
    modes_frame = ctk.CTkFrame(detection_mode_frame, corner_radius=8, fg_color="#f0f0f0")
    modes_frame.pack(pady=3, padx=10, fill="x")

    modes_label = ctk.CTkLabel(
        modes_frame,
        text="Modes",
        text_color=("black"),
        font=ctk.CTkFont(size=14, weight="bold"),
    )
    modes_label.pack(pady=(5, 2), padx=10, anchor="w")


    radio_buttons_frame = ctk.CTkFrame(modes_frame, fg_color="transparent")
    radio_buttons_frame.pack(pady=4, padx=10, fill="x")

    # Configure grid to expand equally
    for i in range(3):
        radio_buttons_frame.columnconfigure(i, weight=1)

    # Add radio buttons in individual frames
    modes = ["Face-Detection-Mode", "Danger-Scan-Mode", "Full-Protection-Mode"]
    detection_mode = tk.StringVar(value="")
    for i, mode in enumerate(modes):
        
        button_frame = ctk.CTkFrame(radio_buttons_frame, fg_color="transparent")
        button_frame.grid(row=0, column=i, sticky="ew", padx=2)
        button_frame.columnconfigure(0, weight=1)
        rb = ctk.CTkRadioButton(
            button_frame, 
            text=mode, 
            variable=detection_mode, 
            value=mode, 
            corner_radius=6,
            text_color=("black"),
            font=ctk.CTkFont(size=12),
            hover_color="#3a7ebf",
            border_width_checked=4
        )
        rb.pack(pady=4, padx=5, anchor="w")  



def close_window():
    global cap_a, cap_b, running_a, running_b
    Start_window.destroy()
    if running_a:
        cap_a.release()
    if running_b:
        cap_b.release()


def show_camera_a_value():
    messagebox.showinfo("Camera A", f"Radio Variable Value: {radio_var.get()}")


def go_sitting():
    Start_window.destroy()
    setting()


def go_Face_Recognition():
    Start_window.destroy()
    face_recording()


def show_camera_b_value():
    global url_1
    if url_1:
        messagebox.showinfo("Camera B", f"Camera B URL: {url_1}")
    else:
        messagebox.showerror("Error", "No camera URL input provided")


def find_names():
    global All_name
    folder_path = os.path.dirname(os.path.realpath(__file__))
    Face_path = os.path.join(folder_path, "database")
    for filename in os.listdir(Face_path):
        if filename.endswith(".jpg"):
            name_without_extension = os.path.splitext(filename)[0]   
            if name_without_extension not in All_name:  
                All_name.append(name_without_extension)  
    return All_name


def exit_sitting():
    if messagebox.askokcancel("Exit", "Do you really want to main manu?"):
        window_setting.destroy()


def face_recording():
    global face_window, label_r, entry_name

    face_window = ctk.CTkToplevel(root)
    face_window.title("face_recording")
    face_window.geometry(f"{1080}x{720}")
    face_window.resizable(False, False)
    find_names()
    load_image()

    bg_image_label = ctk.CTkLabel(
        face_window, text="", image=images_logos["logo_BG_image"]
    )

    bg_image_label.place(
        relx=0, rely=0, relwidth=1, relheight=1
    )  
    bg_image_label.lower()

    logo_frame = ctk.CTkFrame(face_window)
    logo_frame.pack(
        fill="x", pady=(0, 10)
    ) 

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=images_logos["logo_KMITL_image"],
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame,
        text="",
        image=images_logos["logo_RIE_image"],
        fg_color="white",
        corner_radius=20,
    )
    logo_rie_label.pack(side="left", pady=(10, 10))


    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=12, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))

    main_frame = ctk.CTkFrame(face_window, fg_color="black")
    main_frame.pack(fill="y", pady=20) 

    video_frame = ctk.CTkFrame(main_frame, fg_color="#161616")
    video_frame.pack(side="left", fill="y")

    frame_r = ctk.CTkFrame(
        video_frame, width=320, height=320, fg_color="white", corner_radius=20
    )
    frame_r.pack(expand=True, anchor="n", pady=(5, 10), padx=(30, 30))
    label_r = ctk.CTkLabel(
        frame_r, text="", image=images_logos["logo_KMITL_image"], width=320, height=320
    )
    label_r.pack(
        side="top", expand=True, padx=10, pady=10
    )  
    button1 = ctk.CTkButton(frame_r, text="Open Camera", command=toggle_camera_r)
    button1.pack(side="bottom", pady=10)
    exit_bottom = ctk.CTkButton(
        video_frame, text="Exit", command=exit_face, fg_color="red", text_color="black"
    )
    exit_bottom.pack(padx=10, pady=(10, 5))

    input_data_frame = ctk.CTkFrame(main_frame)
    input_data_frame.pack(side="right", fill="y", padx=(30, 30), pady=(5, 10))

    label_name = ctk.CTkLabel(
        input_data_frame, text="Name", font=ctk.CTkFont(size=16, weight="bold")
    )
    label_name.pack(padx=10, pady=5)
    entry_name = ctk.CTkEntry(input_data_frame, placeholder_text="Enter image name")
    entry_name.pack(padx=10, pady=5)

    btn_save_b = ctk.CTkButton(
        input_data_frame,
        text="Save Image",
        command=countdown_and_save,
        fg_color="#3fd956",
        text_color="black",
    )
    btn_save_b.pack(padx=10, pady=(10, 5))

    btn_delete_b = ctk.CTkButton(
        input_data_frame,
        text="Delete Image",
        command=delete_image_face,
        fg_color="red",
        text_color="black",
    )
    btn_delete_b.pack(padx=10, pady=5)

    scrollable_frame = ctk.CTkScrollableFrame(
        input_data_frame, label_text="Database"
    )
    scrollable_frame.pack(padx=10, pady=5)
    for name in range(len(All_name)):
        Name = ctk.CTkLabel(
            scrollable_frame,
            text=f"Person {name+1} : {All_name[name]}",
            font=ctk.CTkFont(size=12, weight="normal"),
        ) 
        Name.pack(padx=10, pady=5)


def exit_face():
    if messagebox.askokcancel("Exit", "Do you really want to main manu?"):
        face_window.destroy()
    if running_r:
        cap_r.release()


def save_image_b():
    global entry_name
    if cap_r is not None and cap_r.isOpened():
        ret, frame = cap_r.read()
        if ret:
            filename = entry_name.get()
            if filename:
                folder_path = os.path.dirname(os.path.realpath(__file__))
                Face_path = os.path.join(folder_path, "database")
                full_filename = os.path.join(Face_path, f"{filename}.jpg")
                logging.info(f"Image saved at: {full_filename}")
                logging.info(f"By : {filename}")
                if os.path.exists(filename):
                    label_r.configure(text="File already exists! Choose another name.") 
                    return
                cv2.imwrite(full_filename, frame)
                print(f"Image saved at: {full_filename}")
                label_r.configure(text="Image saved!")
            else:
                label_r.configure(text="Please enter a name!")


def countdown_and_save():
    countdown(4) 


def countdown(count):
    if count > 0:
        label_r.configure(
            text=f"Saving in {count}...",
            text_color="yellow",
            font=ctk.CTkFont(size=18, weight="bold"),) 
        label_r.after(1000, countdown, count - 1)
    else:
        save_image_b()
        logging.info("Save Image Success")


def delete_image_face():
    filename = entry_name.get()
    if filename:
        if messagebox.askokcancel(
            "Delete !!!", f"Do you really want to delete {filename} ?"):
            for ext in [".jpg", ".jpeg"]:
                file_path = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),  
                    "database",  
                    f"{filename}{ext}", 
                )
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    label_r.configure(text=f"Deleted: {file_path}")
                    return
        messagebox.showerror("Delete !!!", "File not found.")
    else:
        messagebox.showerror("Delete !!!", "Please enter a name!")


def delete_image_sitting():
    filename = entry_name_Delete.get()
    if filename:
        if messagebox.askokcancel(
            "Delete !!!", f"Do you really want to delete {filename}?"):
            for ext in [".jpg", ".jpeg"]:
                file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"database",  f"{filename}{ext}")
                print(file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    messagebox.showinfo("Deleted", f"Deleted: {filename}")
                    return
        messagebox.showerror("Delete !!!", "File not found.")
    else:
        messagebox.showerror("Delete !!!", "Please enter a name!")


def setting():
    global home_frame, second_frame, Third_frame, entry_name, entry_password_sitting, url_1, url_now, entry_name_Delete, window_setting

    window_setting = ctk.CTkToplevel(root)
    window_setting.title("Setting")
    window_setting.geometry("700x550")
    window_setting.resizable(False, False)
    find_names()
    load_image()

    navigation_frame = ctk.CTkFrame(window_setting, corner_radius=20)
    navigation_frame.pack(side="left", fill="y", padx=10, pady=10)


    navigation_frame_label = ctk.CTkLabel(
        navigation_frame,
        text="  SITTING MENU",
        image=images_logos["small_logo_KMITL_image"],
        compound="left",
        font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="white",
        text_color="#000000",
    )
    navigation_frame_label.pack(pady=20, ipadx=20, fill="x")

    home_button = ctk.CTkButton(
        navigation_frame,
        corner_radius=0,
        height=40,
        border_spacing=10,
        text="Home",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray30"),
        image=images_logos["home_logo"],
        anchor="w",
        command=lambda: show_frame("home"),
    )
    home_button.pack(fill="x", pady=5)

    frame_2_button = ctk.CTkButton(
        navigation_frame,
        corner_radius=0,
        height=40,
        border_spacing=10,
        text="Setting",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray30"),
        image=images_logos["address_logo"],
        anchor="w",
        command=lambda: show_frame("frame_2"),
    )
    frame_2_button.pack(fill="x", pady=5)

    frame_3_button = ctk.CTkButton(
        navigation_frame,
        corner_radius=0,
        height=40,
        border_spacing=10,
        text="Face Database",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray30"),
        image=images_logos["sitting_logo"],
        anchor="w",
        command=lambda: show_frame("frame_3"),
    )
    frame_3_button.pack(fill="x", pady=5)

    exit_sitting_Button = ctk.CTkButton(
        navigation_frame,
        text="Exit",
        fg_color="red",
        command=exit_sitting,
        hover_color="#FF9999",
        text_color="#F9FFFC",
    )
    exit_sitting_Button.pack(side="bottom", padx=20, pady=20)

    home_frame = ctk.CTkFrame(window_setting, corner_radius=0, fg_color="transparent")
    home_frame.pack(fill="both", expand=True, padx=20, pady=20)

    mid_frame = ctk.CTkFrame(home_frame, corner_radius=0, fg_color="transparent")
    mid_frame.pack(fill="both", expand=True, padx=20, pady=10)

    center_frame = ctk.CTkFrame(
        mid_frame, corner_radius=20, fg_color="gray50", height=50
    )
    center_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    head_User_manual = ctk.CTkLabel(
        center_frame,
        text="User Manual",
        font=ctk.CTkFont(size=18, weight="bold"),
        corner_radius=40,
    )
    head_User_manual.pack(pady=(10, 10))

    User_manual_frame = ctk.CTkScrollableFrame(
        center_frame, corner_radius=40, fg_color="gray70"
    )
    User_manual_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    User_manual_1 = ctk.CTkLabel(
        User_manual_frame,
        text="1.The user must register the camera at ",
        image=images_logos["address_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_1.pack(pady=(10, 5))

    User_manual_2 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Enter the system user name ",
        image=images_logos["user_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_2.pack(pady=(5, 5))

    User_manual_3 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Enter the system user password ",
        image=images_logos["lock_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_3.pack(pady=(5, 5))

    User_manual_4 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Enter the IP address of the camera user ",
        image=images_logos["IP_address_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_4.pack(pady=(5, 5))

    User_manual_5 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Select the image quality ",
        image=images_logos["sitting_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_5.pack(pady=(5, 5))

    User_manual_6 = ctk.CTkLabel(
        User_manual_frame,
        text="2. The system can detect all 4 types of events",
        font=ctk.CTkFont(size=14),
        text_color="black",
    )
    User_manual_6.pack(pady=(10, 5))

    User_manual_7 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Person fall  ",
        image=images_logos["rescue_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
        anchor="w",
    )
    User_manual_7.pack(pady=(5, 5))

    User_manual_8 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Snake  ",
        image=images_logos["snake_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
        anchor="w",
    )
    User_manual_8.pack(pady=(5, 5))

    User_manual_9 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Baby vomit  ",
        image=images_logos["baby_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
        anchor="w",
    )
    User_manual_9.pack(pady=(5, 5))

    User_manual_10 = ctk.CTkLabel(
        User_manual_frame,
        text="    • Stranger  ",
        image=images_logos["bandit_logo"],
        compound="right",
        font=ctk.CTkFont(size=14),
        text_color="black",
        anchor="w",
    )
    User_manual_10.pack(pady=(5, 10))

    left_frame = ctk.CTkFrame(
        mid_frame,
        corner_radius=30,
        fg_color=("gray70", "gray30"),
        height=150,
        width=100,
    )
    left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

    mode_event = ctk.CTkLabel(
        left_frame,
        text="",
        image=images_logos["mode_event_icon"],
        width=100,
        font=ctk.CTkFont(size=14),
    )
    mode_event.pack(pady=(5, 10))

    appearance_mode_menu = ctk.CTkOptionMenu(
        left_frame,
        values=["Light", "Dark", "System"],
        command=change_appearance_mode_event,
        width=100,
    )
    appearance_mode_menu.pack(pady=(5, 10)) 
    appearance_mode_menu.set("Light")

    right_frame = ctk.CTkFrame(
        mid_frame,
        corner_radius=30,
        fg_color=("gray70", "gray30"),
        height=150,
        width=100,
    )
    right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=10)

    loupe_event = ctk.CTkLabel(
        right_frame,
        text="",
        image=images_logos["loupe_logo"],
        width=100,
        font=ctk.CTkFont(size=14),
    )
    loupe_event.pack(pady=(5, 10))

    scaling_optionemenu = ctk.CTkOptionMenu(
        right_frame,
        values=["80%", "90%", "100%"],
        command=change_scaling_event,
        width=100,
    )
    scaling_optionemenu.pack(pady=(10, 10))
    scaling_optionemenu.set("100%")

    second_frame = ctk.CTkFrame(window_setting, corner_radius=0, fg_color="transparent")
    second_frame.pack(fill="both", expand=True)

    tabview = ctk.CTkTabview(second_frame,corner_radius=5)
    tabview.pack(padx=(5, 5), pady=(10, 10))
    tabview.add("Camera 1")
    tabview.add("Camera 2")
    tabview.add("Camera 3")
    tabview.add("Camera 4")
    tabview.add("Camera 5")
    tabview.add("Camera 6")


    label_Head = ctk.CTkLabel(tabview.tab("Camera 1"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)
    label_Head = ctk.CTkLabel(tabview.tab("Camera 2"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)
    label_Head = ctk.CTkLabel(tabview.tab("Camera 3"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)
    label_Head = ctk.CTkLabel(tabview.tab("Camera 4"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)
    label_Head = ctk.CTkLabel(tabview.tab("Camera 5"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)
    label_Head = ctk.CTkLabel(tabview.tab("Camera 6"), text="Enter connection data", font=ctk.CTkFont(size=24, weight="bold"))
    label_Head.pack(padx=10, pady=5)

    label_width = 80 

    name_frame = ctk.CTkFrame(tabview.tab("Camera 1"), fg_color="transparent")
    name_frame.pack(padx=10, pady=5, fill="x")

    label_name = ctk.CTkLabel(name_frame, text=" Name", image=images_logos["user_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_name.pack(side="left", padx=10, pady=5)

    entry_name = ctk.CTkEntry(name_frame, placeholder_text="Enter name")
    entry_name.pack(side="left", fill="x", expand=True, padx=10)

    password_frame = ctk.CTkFrame(tabview.tab("Camera 1"), fg_color="transparent")
    password_frame.pack(padx=10, pady=5, fill="x")

    label_password = ctk.CTkLabel(password_frame, text=" Password", image=images_logos["lock_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_password.pack(side="left", padx=10, pady=5)

    entry_password_sitting = ctk.CTkEntry(password_frame, show="*", placeholder_text="Enter password")
    entry_password_sitting.pack(side="left", fill="x", expand=True, padx=10)


    button_frame = ctk.CTkFrame(tabview.tab("Camera 1"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")

    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_1)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)


    port_frame = ctk.CTkFrame(tabview.tab("Camera 1"), fg_color="transparent")
    port_frame.pack(padx=10, pady=5, fill="x")

    label_port = ctk.CTkLabel(port_frame, text=" Quality", image=images_logos["sitting_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_port.pack(side="left", padx=10, pady=5)


    quality_values = ["Select Quality", "High Quality", "High Performance"]
    optionmenu_quality_values = ctk.CTkOptionMenu(port_frame, dynamic_resizing=True, values=quality_values,command=quality_selected)
    optionmenu_quality_values.pack(side="left", fill="x", expand=True, padx=10)

    agree_button = ctk.CTkButton(tabview.tab("Camera 1"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_1)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)


    button_frame = ctk.CTkFrame(tabview.tab("Camera 2"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")

    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_2)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)
    
    agree_button = ctk.CTkButton(tabview.tab("Camera 2"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_2)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)


    button_frame = ctk.CTkFrame(tabview.tab("Camera 3"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")

    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_3)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)
    
    agree_button = ctk.CTkButton(tabview.tab("Camera 3"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_3)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)



    button_frame = ctk.CTkFrame(tabview.tab("Camera 4"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")

    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_4)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)

    agree_button = ctk.CTkButton(tabview.tab("Camera 4"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_4)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)



    button_frame = ctk.CTkFrame(tabview.tab("Camera 5"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")

    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_5)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)
    
    agree_button = ctk.CTkButton(tabview.tab("Camera 5"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_5)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)



    button_frame = ctk.CTkFrame(tabview.tab("Camera 6"), fg_color="transparent")
    button_frame.pack(padx=10, pady=5, fill="x")
    
    label_button = ctk.CTkLabel(button_frame, text=" IP", image=images_logos["address_logo"], compound="left", width=label_width, anchor="w", font=ctk.CTkFont(size=14))
    label_button.pack(side="left", padx=10, pady=5)

    string_input_button = ctk.CTkButton(button_frame, text="Open Address",command=input_dialog_Address_6)
    string_input_button.pack(side="left", fill="x", expand=True, padx=10)
    
    agree_button = ctk.CTkButton(tabview.tab("Camera 6"), text="agree", fg_color="green", hover_color="#46b842",command=combine_button_6)
    agree_button.pack(pady=10,fill="x", expand=True,padx=40)
    

    label_port = ctk.CTkLabel(
        second_frame,
        text="In general, the RTSP link will have the following appearance \n rtsp://Rachata:123456@198.162.0.100:554/stream1 \n It can be divided as follows \n rtsp:// username: password @ ip_camera: port(554) / quality",
        font=ctk.CTkFont(size=14),
    )
    label_port.pack(padx=10, pady=5)

    url_now = ctk.CTkLabel(
        second_frame, text=f" Your RTSP link is \n {url_1}", font=ctk.CTkFont(size=14)
    )
    url_now.pack(padx=10, pady=5)

    Third_frame = ctk.CTkFrame(window_setting, corner_radius=0, fg_color="transparent")

    main_frame_Third = ctk.CTkFrame(Third_frame, corner_radius=30, fg_color="gray")
    main_frame_Third.pack(pady=20, padx=10, fill="both", expand=True)

    Delete_Image_button = ctk.CTkButton(
        main_frame_Third, text="Delete Image", command=delete_image_sitting
    )
    Delete_Image_button.pack(
        side="bottom", fill="both", pady=(10, 20), padx=30, expand=True, anchor="s"
    )

    entry_name_Delete = ctk.CTkEntry(main_frame_Third, placeholder_text="Enter Name")
    entry_name_Delete.pack(
        side="bottom", fill="x", expand=True, padx=30, anchor="s", pady=(10, 0)
    )

    lable_ScrollableFrame = ctk.CTkLabel(
        main_frame_Third,
        text="List of registered people",
        font=ctk.CTkFont(size=25, weight="bold"),
    )
    lable_ScrollableFrame.pack(padx=10, pady=5)

    mane_frame_Third = ctk.CTkScrollableFrame(
        main_frame_Third, corner_radius=30, fg_color="gray70"
    )
    mane_frame_Third.pack(pady=10, padx=20, fill="both", expand=True)

    for name in range(len(All_name)):
        Name_sitting = ctk.CTkLabel(
            mane_frame_Third,
            text=f"Person {name+1} : {All_name[name]}",
            font=ctk.CTkFont(size=16, weight="normal"),
            text_color="black",
        )
        Name_sitting.pack(padx=10, pady=5)


def detect_bounding_box(frame):
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_classifier.detectMultiScale(frame, 1.1, 5, minSize=(40, 40))
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    return frame


def on_radio_select(*args):
    global selected_value
    selected_value = radio_var.get()


radio_var = tk.IntVar(value=0)
radio_var.trace("w", on_radio_select)


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    ctk.set_widget_scaling(new_scaling_float)


def input_dialog_Address_1():
    global ip_camera_url_1
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_1 = dialog.get_input()
    if address_1:
        ip_camera_url_1 = address_1
        print("Address :", ip_camera_url_1)
        logging.info(f"Received IP Address of Camera 1: {ip_camera_url_1}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 1")

def input_dialog_Address_2():
    global ip_camera_url_2
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_2 = dialog.get_input()
    if address_2:
        ip_camera_url_2 = address_2
        print("Address :", ip_camera_url_2)
        logging.info(f"Received IP Address of Camera 2: {ip_camera_url_2}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 2")

def input_dialog_Address_3():
    global ip_camera_url_3
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_3 = dialog.get_input()
    if address_3:
        ip_camera_url_3 = address_3
        print("Address :", ip_camera_url_3)
        logging.info(f"Received IP Address of Camera 3: {ip_camera_url_3}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 3")


def input_dialog_Address_4():
    global ip_camera_url_4
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_4 = dialog.get_input()
    if address_4:
        ip_camera_url_4 = address_4
        print("Address :", ip_camera_url_4)
        logging.info(f"Received IP Address of Camera 4: {ip_camera_url_4}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 4")


def input_dialog_Address_5():
    global ip_camera_url_5
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_5 = dialog.get_input()
    if address_5:
        ip_camera_url_5 = address_5
        print("Address :", ip_camera_url_5)
        logging.info(f"Received IP Address of Camera 5: {ip_camera_url_5}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 5")


def input_dialog_Address_6():
    global ip_camera_url_6
    dialog = ctk.CTkInputDialog(text="Type in a number of IP Address \n example : 192.168.0.102" , title="Address")
    address_6 = dialog.get_input()
    if address_6:
        ip_camera_url_6 = address_6
        print("Address :", ip_camera_url_6)
        logging.info(f"Received IP Address of Camera 6: {ip_camera_url_6}")
    else:
        print("No address input received")
        logging.error("No IP Address received for Camera 6")


def combine_button_1():
    global url_1, entry_name, entry_password_sitting, global_selected_quality, url_now , ip_camera_url_1
    if ip_camera_url_1 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_1 = f'rtsp://{name}:{password}@{ip_camera_url_1}:554/{global_selected_quality}'
        print("Address:", url_1)
        url_now.configure(text=f"Your RTSP link is \n {url_1}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def combine_button_2():
    global url_2, entry_name, entry_password_sitting, global_selected_quality, url_now 
    if ip_camera_url_2 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_2 = f'rtsp://{name}:{password}@{ip_camera_url_2}:554/{global_selected_quality}'
        print("Address:", url_2)

        url_now.configure(text=f"Your RTSP link is \n {url_2}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def combine_button_3():
    global url_3, entry_name, entry_password_sitting, global_selected_quality, url_now 
    if ip_camera_url_3 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_3 = f'rtsp://{name}:{password}@{ip_camera_url_3}:554/{global_selected_quality}'
        print("Address:", url_3)
        
        
        url_now.configure(text=f"Your RTSP link is \n {url_3}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def combine_button_4():
    global url_4, entry_name, entry_password_sitting, global_selected_quality, url_now 
    if ip_camera_url_4 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_4 = f'rtsp://{name}:{password}@{ip_camera_url_4}:554/{global_selected_quality}'
        print("Address:", url_4)
        
        
        url_now.configure(text=f"Your RTSP link is \n {url_4}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def combine_button_5():
    global url_5, entry_name, entry_password_sitting, global_selected_quality, url_now 
    if ip_camera_url_5 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_5 = f'rtsp://{name}:{password}@{ip_camera_url_5}:554/{global_selected_quality}'
        print("Address:", url_5)
        
        
        url_now.configure(text=f"Your RTSP link is \n {url_5}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def combine_button_6():
    global url_6, entry_name, entry_password_sitting, global_selected_quality, url_now 
    if ip_camera_url_6 and entry_name and entry_password_sitting:
        if not global_selected_quality:
            global_selected_quality = "stream2"
        name = entry_name.get()  
        password = entry_password_sitting.get() 
        url_6 = f'rtsp://{name}:{password}@{ip_camera_url_6}:554/{global_selected_quality}'
        print("Address:", url_6)
        
        
        url_now.configure(text=f"Your RTSP link is \n {url_6}")
    else:
        print("No address input received")
        messagebox.showerror("Error", "No address input received")


def exit_program():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy() 
        logging.info("Closing program")
        logging.info("=========================================================================")


def change_appearance_mode_event(new_appearance_mode: str):
    logging.info(f"Changing appearance mode to {new_appearance_mode}")
    ctk.set_appearance_mode(new_appearance_mode)


def Main_window():
    ctk.set_appearance_mode("Light")
    root.title("Security System")
    root.geometry("1000x700")
    root.resizable(False, False)
    load_image()


    bg_image_label = ctk.CTkLabel(root, text="", image=images_logos["logo_BG_image"])
    bg_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    bg_image_label.lower()

    main_container = ctk.CTkFrame(root, fg_color=("#ffffff", "#01061d"))
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    header_frame = ctk.CTkFrame(
        main_container, corner_radius=15, fg_color=("#ffffff", "#01061d"), height=150
    )
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)

    logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
    logo_container.pack(fill="x", padx=20, pady=10)

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_container,
        text="",
        image=images_logos["logo_KMITL_image"],
        fg_color=("#ffffff"),
        corner_radius=15,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=(0, 20))

    logo_rie_label = ctk.CTkLabel(
        logo_container,
        text="",
        image=images_logos["logo_RIE_image"],
        fg_color=("#ffffff"),
        corner_radius=15,
    )
    logo_rie_label.pack(side="left", padx=(0, 20))

    text_container = ctk.CTkFrame(logo_container, fg_color="transparent")
    text_container.pack(side="left", fill="both", expand=True)

    text_rie_label = ctk.CTkLabel(
        text_container,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus",
        font=ctk.CTkFont(family="FC Minimal", size=13, weight="bold"),
        justify="left",
        text_color=("#E35205", "#F9FFFC"),
    )
    text_rie_label.pack(anchor="w", pady=(50, 10))

    subtitle_label = ctk.CTkLabel(
        text_container,
        text="Robotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(family="FC Minimal", size=16, weight="bold"),
        justify="left",
        text_color=("#E35205", "#F9FFFC"),
    )
    subtitle_label.pack(anchor="w")

    menu_frame = ctk.CTkFrame(
        main_container,
        corner_radius=20,
        fg_color=("#ffffff", "#1D1B26"),
        border_width=2,
        border_color=("#333333", "#F9FFFC"),
    )
    menu_frame.pack(pady=20, padx=100)

    logo_label = ctk.CTkLabel(
        menu_frame,
        text="Security System",
        font=ctk.CTkFont(family="FC Minimal", size=48, weight="bold"),
        text_color="#E35205",
    )
    logo_label.pack(padx=40, pady=30)

    button_style = {
        "height": 40,
        "width": 200,
        "corner_radius": 10,
        "font": ctk.CTkFont(family="FC Minimal", size=16, weight="bold"),
        "border_width": 2,
        "text_color": "#F9FFFC",
    }

    start_button = ctk.CTkButton(
        menu_frame,
        text="Start",
        fg_color=("#E35205", "#C24504"),
        hover_color="#45a049",
        border_color="#333333",
        command=start,
        **button_style,
    )
    start_button.pack(pady=10)

    face_rec_button = ctk.CTkButton(
        menu_frame,
        text="Face Recognition",
        fg_color=("#E35205", "#C24504"),
        hover_color="#1976D2",
        border_color="#333333",
        command=face_recording,
        **button_style,
    )
    face_rec_button.pack(pady=10)

    setting_button = ctk.CTkButton(
        menu_frame,
        text="Setting",
        fg_color=("#E35205", "#C24504"),
        hover_color="#FFA000",
        border_color="#333333",
        command=setting,
        **button_style,
    )
    setting_button.pack(pady=10)


    exit_button = ctk.CTkButton(
        menu_frame,
        text="Exit",
        fg_color=("#E35205", "#C24504"),
        hover_color="#d32f2f",
        border_color="#333333",
        command=exit_program,
        **button_style,
    )
    exit_button.pack(pady=(10, 30))

    root.mainloop()


def Additional_Detection_1():
    global Additional , label_c
    clear_window()

    Additional = ctk.CTkToplevel(root)
    Additional.title("Additional Detection")

    screen_width = Additional.winfo_screenwidth() / 2
    screen_height = Additional.winfo_screenheight() / 2


    Additional.geometry(f"{screen_width}x{screen_height}")

    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

    logo_KMITL_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(130, 130)
    )
    logo_RIE_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(130, 130)
    )

    logo_frame = ctk.CTkFrame(Additional)
    logo_frame.pack(fill="x", pady=(0, 10))

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=logo_KMITL_image,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame, text="", image=logo_RIE_image, fg_color="white", corner_radius=20
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))


    video_container = ctk.CTkFrame(Additional)
    video_container.pack(fill="both", expand=True, pady=20)

    frame_c = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_c.pack(side="top", expand=True, anchor="center", pady=(5, 10), padx=30)

    label_c = ctk.CTkLabel(
        frame_c, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_c.pack(side="top", expand=True, pady=(10, 0))


    button1 = ctk.CTkButton(frame_c, text="Open Camera 3", command=toggle_camera_c)
    button1.pack(side="bottom", pady=(10, 10))

    menu_frame = ctk.CTkFrame(Additional, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)


    add_camera_button = ctk.CTkButton(
        menu_frame, text="Add Camera", corner_radius=5, width=15, command=add_camera_frames
    )
    add_camera_button.pack(side="left", padx=10, pady=10)
    
    back_button = ctk.CTkButton(
        menu_frame, text="Back", corner_radius=5, width=15, command=exit_Additional
    )
    back_button.pack(side="left", padx=10, pady=10)


def additional_Detection_2():
    global Additional , label_c , label_d
    clear_window()

    screen_width = Additional.winfo_screenwidth() / 2
    screen_height = Additional.winfo_screenheight() / 2

    
    Additional.geometry(f"{screen_width}x{screen_height}")

    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

    
    logo_KMITL_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(130, 130)
    )
    logo_RIE_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(130, 130)
    )

    
    logo_frame = ctk.CTkFrame(Additional)
    logo_frame.pack(fill="x", pady=(0, 10))

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=logo_KMITL_image,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame, text="", image=logo_RIE_image, fg_color="white", corner_radius=20
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))

    
    video_container = ctk.CTkFrame(Additional)
    video_container.pack(fill="both", expand=True, pady=20)

    
    frame_c = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_c.pack(side="left", expand=True, anchor="center", pady=(5, 10), padx=(30, 15))

    label_c = ctk.CTkLabel(
        frame_c, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_c.pack(side="top", expand=True, pady=(10, 0))

    buttonc = ctk.CTkButton(frame_c, text="Open Camera 3")
    buttonc.pack(side="bottom", pady=(10, 10))

    
    frame_d = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_d.pack(side="left", expand=True, anchor="center", pady=(5, 10), padx=(15, 30))

    label_d = ctk.CTkLabel(
        frame_d, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_d.pack(side="top", expand=True, pady=(10, 0))

    buttond = ctk.CTkButton(frame_d, text="Open Camera 4")
    buttond.pack(side="bottom", pady=(10, 10))

    
    menu_frame = ctk.CTkFrame(Additional, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)

    
    add_camera_button = ctk.CTkButton(
            menu_frame, text="Add Camera", corner_radius=5, width=15, command=add_camera_frames
    )
    add_camera_button.pack(side="left", padx=10, pady=10)


    back_button = ctk.CTkButton(
        menu_frame, text="Back", corner_radius=5, width=15, command=exit_Additional
    )
    back_button.pack(side="left", padx=10, pady=10)


def additional_Detection_3():
    global Additional , label_c , label_d , label_e
    clear_window()

    screen_width = Additional.winfo_screenwidth() / 2
    screen_height = Additional.winfo_screenheight() / 2

    
    Additional.geometry(f"{screen_width}x{screen_height}")

    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

    
    logo_KMITL_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(130, 130)
    )
    logo_RIE_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(130, 130)
    )

    
    logo_frame = ctk.CTkFrame(Additional)
    logo_frame.pack(fill="x", pady=(0, 10))

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=logo_KMITL_image,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame, text="", image=logo_RIE_image, fg_color="white", corner_radius=20
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))

    
    video_container = ctk.CTkFrame(Additional)
    video_container.pack(fill="both", expand=True, pady=20)

    
    frame_c = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_c.pack(side="left", expand=True, anchor="center", pady=(5, 10), padx=(20, 10))

    label_c = ctk.CTkLabel(
        frame_c, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_c.pack(side="top", expand=True, pady=(10, 0))

    buttonc = ctk.CTkButton(frame_c, text="Open Camera 3")
    buttonc.pack(side="bottom", pady=(10, 10))

    
    frame_d = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_d.pack(side="left", expand=True, anchor="center", pady=(5, 10), padx=(10, 10))

    label_d = ctk.CTkLabel(
        frame_d, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_d.pack(side="top", expand=True, pady=(10, 0))

    buttond = ctk.CTkButton(frame_d, text="Open Camera 4")
    buttond.pack(side="bottom", pady=(10, 10))

    
    frame_e = ctk.CTkFrame(
        video_container, width=350, height=320, fg_color="white", corner_radius=10
    )
    frame_e.pack(side="left", expand=True, anchor="center", pady=(5, 10), padx=(10, 20))

    label_e = ctk.CTkLabel(
        frame_e, text="", image=logo_KMITL_image, width=300, height=310
    )
    label_e.pack(side="top", expand=True, pady=(10, 0))

    buttone = ctk.CTkButton(frame_e, text="Open Camera 5")
    buttone.pack(side="bottom", pady=(10, 10))

    
    menu_frame = ctk.CTkFrame(Additional, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)

    
    add_camera_button = ctk.CTkButton(
        menu_frame, text="Add Camera", corner_radius=5, width=15, command=add_camera_frames
    )
    add_camera_button.pack(side="left", padx=10, pady=10)

    
    back_button = ctk.CTkButton(
        menu_frame, text="Back", corner_radius=5, width=15, command=exit_Additional
    )
    back_button.pack(side="left", padx=10, pady=10)


def additional_Detection_4():
    global Additional , label_c , label_d , label_e , label_f
    clear_window()

    screen_width = Additional.winfo_screenwidth() / 2
    screen_height = Additional.winfo_screenheight() / 2

    
    Additional.geometry(f"{screen_width}x{screen_height}")

    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

    
    logo_KMITL_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(100, 100)
    )
    logo_RIE_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(100, 100)
    )

    
    logo_frame = ctk.CTkFrame(Additional)
    logo_frame.pack(fill="x", pady=(0, 10))

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=logo_KMITL_image,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame, text="", image=logo_RIE_image, fg_color="white", corner_radius=20
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))

    
    video_container = ctk.CTkFrame(Additional)
    video_container.pack(fill="both", expand=True)


    top_container = ctk.CTkFrame(video_container)
    top_container.pack(fill="x", expand=True, pady=(10, 5))


    frame_c = ctk.CTkFrame(
        top_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_c.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_c = ctk.CTkLabel(
        frame_c, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_c.pack(side="top", expand=True, pady=(10, 0))

    buttonc = ctk.CTkButton(frame_c, text="Open Camera 1")
    buttonc.pack(side="bottom", pady=(10, 10))

    frame_d = ctk.CTkFrame(
        top_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_d.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_d = ctk.CTkLabel(
        frame_d, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_d.pack(side="top", expand=True, pady=(10, 0))

    buttond = ctk.CTkButton(frame_d, text="Open Camera 2")
    buttond.pack(side="bottom", pady=(10, 10))


    bottom_container = ctk.CTkFrame(video_container)
    bottom_container.pack(fill="x", expand=True, pady=(5, 10))


    frame_e = ctk.CTkFrame(
        bottom_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_e.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_e = ctk.CTkLabel(
        frame_e, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_e.pack(side="top", expand=True, pady=(10, 0))

    buttone = ctk.CTkButton(frame_e, text="Open Camera 3")
    buttone.pack(side="bottom", pady=(10, 10))


    frame_f = ctk.CTkFrame(
        bottom_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_f.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_f = ctk.CTkLabel(
        frame_f, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_f.pack(side="top", expand=True, pady=(10, 0))

    buttonf = ctk.CTkButton(frame_f, text="Open Camera 4")
    buttonf.pack(side="bottom", pady=(10, 10))

    
    menu_frame = ctk.CTkFrame(Additional, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)

    
    add_camera_button = ctk.CTkButton(
        menu_frame, text="Add Camera", corner_radius=5, width=15, command=add_camera_frames
    )
    add_camera_button.pack(side="left", padx=10, pady=10)

    
    back_button = ctk.CTkButton(
        menu_frame, text="Back", corner_radius=5, width=15, command=exit_Additional
    )
    back_button.pack(side="left", padx=10, pady=10)


def additional_Detection_5():
    global Additional , label_c , label_d , label_e , label_f , label_g
    clear_window()

    screen_width = Additional.winfo_screenwidth() / 2
    screen_height = Additional.winfo_screenheight() / 2

    
    Additional.geometry(f"{screen_width}x{screen_height}")

    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

    
    logo_KMITL_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "KMITL-Photoroom.png")), size=(100, 100)
    )
    logo_RIE_image = ctk.CTkImage(
        Image.open(os.path.join(image_path, "RIE-Photoroom.png")), size=(100, 100)
    )

    
    logo_frame = ctk.CTkFrame(Additional)
    logo_frame.pack(fill="x", pady=(0, 10))

    navigation_frame_label_KMITL = ctk.CTkLabel(
        logo_frame,
        text="",
        image=logo_KMITL_image,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",
        corner_radius=20,
    )
    navigation_frame_label_KMITL.pack(side="left", padx=20, pady=(10, 10))

    logo_rie_label = ctk.CTkLabel(
        logo_frame, text="", image=logo_RIE_image, fg_color="white", corner_radius=20
    )
    logo_rie_label.pack(side="left", pady=(10, 10))

    text_rie_label = ctk.CTkLabel(
        logo_frame,
        text="King Mongkut's Institute of Technology Ladkrabang Prince of Chumphon Campus \nRobotics and Intelligent Electronics Engineering",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="left",
    )
    text_rie_label.pack(side="left", padx=10, pady=(10, 10))

    
    video_container = ctk.CTkFrame(Additional)
    video_container.pack(fill="both", expand=True)


    top_container = ctk.CTkFrame(video_container)
    top_container.pack(fill="x", expand=True, pady=(10, 5))


    frame_c = ctk.CTkFrame(
        top_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_c.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_c = ctk.CTkLabel(
        frame_c, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_c.pack(side="top", expand=True, pady=(10, 0))

    buttonc = ctk.CTkButton(frame_c, text="Open Camera 1")
    buttonc.pack(side="bottom", pady=(10, 10))

    frame_d = ctk.CTkFrame(
        top_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_d.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_d = ctk.CTkLabel(
        frame_d, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_d.pack(side="top", expand=True, pady=(10, 0))

    buttond = ctk.CTkButton(frame_d, text="Open Camera 2")
    buttond.pack(side="bottom", pady=(10, 10))

    frame_e = ctk.CTkFrame(
        top_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_e.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_e = ctk.CTkLabel(
        frame_e, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_e.pack(side="top", expand=True, pady=(10, 0))

    buttone = ctk.CTkButton(frame_e, text="Open Camera 3")
    buttone.pack(side="bottom", pady=(10, 10))

    bottom_container = ctk.CTkFrame(video_container)
    bottom_container.pack(fill="x", expand=True, pady=(5, 10))

    frame_f = ctk.CTkFrame(
        bottom_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_f.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_f = ctk.CTkLabel(
        frame_f, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_f.pack(side="top", expand=True, pady=(10, 0))

    buttonf = ctk.CTkButton(frame_f, text="Open Camera 4")
    buttonf.pack(side="bottom", pady=(10, 10))

    frame_g = ctk.CTkFrame(
        bottom_container, width=300, height=200, fg_color="white", corner_radius=10
    )
    frame_g.pack(side="left", expand=True, anchor="center", pady=5, padx=5)

    label_g = ctk.CTkLabel(
        frame_g, text="", image=logo_KMITL_image, width=250, height=190
    )
    label_g.pack(side="top", expand=True, pady=(10, 0))

    buttong = ctk.CTkButton(frame_g, text="Open Camera 5")
    buttong.pack(side="bottom", pady=(10, 10))

    
    menu_frame = ctk.CTkFrame(Additional, height=100)
    menu_frame.pack(pady=5, fill="y", side="top", padx=10)

    
    add_camera_button = ctk.CTkButton(
        menu_frame, text="Add Camera", corner_radius=5, width=15, command=add_camera_frames
    )
    add_camera_button.pack(side="left", padx=10, pady=10)

    back_button = ctk.CTkButton(
        menu_frame, text="Back", corner_radius=5, width=15, command=exit_Additional
    )
    back_button.pack(side="left", padx=10, pady=10)


def clear_window():
    global Additional
    if Additional is not None:
        for widget in Additional.winfo_children():
            widget.destroy()


def add_camera_frames():
    global Additional
    num_frames = simpledialog.askinteger(
        "Add Camera", "Enter the number of cameras (1-5):", minvalue=1, maxvalue=5
    )
    if num_frames == 1:
        Additional.destroy()
        Additional = None
        Additional_Detection_1()
    elif num_frames == 2:
        additional_Detection_2()
    if num_frames == 3:
        additional_Detection_3()
    elif num_frames == 4:
        additional_Detection_4()
    if num_frames == 5:
        additional_Detection_5()


def exit_Additional():
    global Additional
    Additional.destroy()
    Additional = None

if __name__ == "__main__":
    try:
        logging.info("Starting the program")
        Main_window()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", "An error occurred while running the program.")
        exit_program()
        logging.info("=========================================================================")



