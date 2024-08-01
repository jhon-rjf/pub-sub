import paho.mqtt.client as mqtt
import cv2
import numpy as np
import base64

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("image/topic")

def on_message(client, userdata, msg):
    # Base64 디코딩
    img_bytes = base64.b64decode(msg.payload)
    # NumPy array로 변환
    npimg = np.frombuffer(img_bytes, dtype=np.uint8)
    # OpenCV를 이용하여 이미지 디코딩
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imshow('Received Image', img)
    cv2.waitKey(100)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()

