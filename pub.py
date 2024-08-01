import paho.mqtt.client as mqtt
import cv2
import base64
import time

# MQTT 설정
mqttc = mqtt.Client()
mqttc.connect("test.mosquitto.org", 1883)
mqttc.loop_start()  # 백그라운드에서 MQTT 루프 실행

# 동영상 파일 열기
cap = cv2.VideoCapture('video.mp4')

def publish_image(image_data):
    # Base64 인코딩
    _, img_encoded = cv2.imencode('.jpg', image_data)
    base64_encoded_image = base64.b64encode(img_encoded).decode('utf-8')

    # MQTT 메시지 발행
    mqttc.publish("image/topic", base64_encoded_image)

# 메인 루프
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 전송
    publish_image(frame)

    time.sleep(0.1)

cap.release()
mqttc.loop_stop()

