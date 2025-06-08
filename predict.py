from ultralytics import YOLO
model = YOLO("model.pt")
model.predict(source = "C:/Users/Hp/Desktop/MAIN_PROJECT2025/DATA/126.jpg",show=True,save=True,conf=0.6,line_width = 1)

