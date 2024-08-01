******
filename: mqtt_yolo_detection.py
How to run: python mqtt_yolo_detection.py
dev: YunK
*******

import paho.mqtt.client as mqtt
import cv2
import numpy as np
import base64
from datetime import datetime
from ultralytics import YOLO
import time

# YOLO 모델 로드
model = YOLO('yolov8n.pt')
last_processed_time = time.time()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe("image/topic")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global last_processed_time
    current_time = time.time()

    # 1초마다 처리
    if current_time - last_processed_time >= 1:
        last_processed_time = current_time

        # 현재 시간 기록
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 이미지 데이터 디코딩 및 처리
        img_bytes = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # YOLO 모델로 객체 탐지
        results = model(img)

        person_count = 0

        # YOLOv8 결과가 리스트인 경우 처리
        for result in results:
            boxes = result.boxes if hasattr(result, 'boxes') else []

            # 탐지 결과에서 사람 수 카운트
            for box in boxes:
                cls = int(box.cls.item())
                if model.names[cls] == 'person':
                    person_count += 1

        print(f'Time: {timestamp}, Person count: {person_count}')

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 연결 정보 설정
broker_address = "test.mosquitto.org"
port = 1883
keepalive = 60

# 연결 시도
try:
    client.connect(broker_address, port, keepalive)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")

# 메시지 루프 시작
client.loop_forever()

