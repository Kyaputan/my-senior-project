from ultralytics import YOLO , RTDETR
import os

folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
models_path = os.path.join(folder_path, "models")

model_path = os.path.join(models_path, "ModelYolo.pt")

model = YOLO(model_path)

model.export(format="onnx", simplify=True, imgsz=640, dynamic=False, nms=True)




