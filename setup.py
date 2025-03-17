import os
import subprocess

folder_1 = "Face_reg"
folder_2 = "img-cap"

now_path = os.path.dirname(os.path.realpath(__file__))

folder_1_path = os.path.join(now_path, folder_1)
folder_2_path = os.path.join(now_path, folder_2)

for folder, path in [(folder_1, folder_1_path), (folder_2, folder_2_path)]:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ สร้างโฟลเดอร์ {folder} ใน {now_path} เสร็จสิ้น")
    else:
        print(f"⚠️ พบ {path} แล้ว ไม่ทำการสร้างซ้ำ")

requirements_path = os.path.join(now_path, "requirements.txt")

if os.path.exists(requirements_path):
    print("📦 กำลังติดตั้ง dependencies จาก requirements.txt ...")
    subprocess.run(["pip", "install", "-r", requirements_path], check=True)
    print("✅ ติดตั้ง dependencies เสร็จสิ้น!")
else:
    print("⚠️ ไม่พบไฟล์ requirements.txt ข้ามขั้นตอนการติดตั้ง dependencies")
