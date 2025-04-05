import face_recognition
import cv2
import numpy as np
import os
import time
import logging
from tkinter import messagebox

face_locations = []
face_encodings = []
known_face_images = []
known_face_encodings = []
known_face_names = []
last_known_notified_time = last_unknown_notified_time = 0
unknown_frame_count = known_frame_count = 0
folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def find_known_face_names():
    folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    Face_path = os.path.join(folder_path, "database")
    image_count = 0
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

                    img_folder = os.path.join(folder_path, "snapshots")
                    img_unknow = os.path.join(img_folder, f"Unknow_{int(time.time())}.jpg")
                    frame_rgb = frame[:, :, :]
                    cv2.imwrite(img_unknow, frame_rgb)
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
                    
                    img_folder = os.path.join(folder_path, "snapshots")
                    img_know = os.path.join(img_folder, f"Known_{name}_{int(time.time())}.jpg")
                    frame_rgb = frame[:, :, :]
                    cv2.imwrite(img_know, frame_rgb)
                    known_frame_count = 0
                    last_known_notified_time = current_time
    return frame

if __name__ == "__main__":
    find_known_face_names()
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        frame = face_recog(frame)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
