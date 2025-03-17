import os


folder_1 = "Face_reg"
folder_2 = "img-cap"

now_path = os.path.dirname(os.path.realpath(__file__))


folder_1_path = os.path.join(now_path, folder_1)
folder_2_path = os.path.join(now_path, folder_2)

if not os.path.exists(folder_1_path):
    os.makedirs(folder_1_path)
    print(f"สร้างโฟลเดอร์ {folder_1} ใน {now_path} เสร็จสิ้น")
else:
    print(f"พบ {folder_1_path} ไม่ทำการสร้างซ้ำ")
    
if not os.path.exists(folder_2_path):
    os.makedirs(folder_2_path)
    print(f"สร้างโฟลเดอร์ {folder_2} ใน {now_path} เสร็จสิ้น")
else:
    print(f"พบ {folder_2_path} ไม่ทำการสร้างซ้ำ")
