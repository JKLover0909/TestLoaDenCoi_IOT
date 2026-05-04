import paho.mqtt.client as mqtt
import json

broker = "45.117.170.179"
port = 1883
topic = "MGSP-V1/F055CF453AB4/cmd"

message = {
    "request_id": "999",
    "audio_stream": {
        "url": "http://192.168.10.4:8090/2.mp3"
    }
}

# ===== Callback khi connect =====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Kết nối MQTT broker thành công")
    else:
        print(f"❌ Kết nối thất bại, mã lỗi: {rc}")

# ===== Callback khi disconnect =====
def on_disconnect(client, userdata, rc):
    print(f"⚠️ Đã disconnect khỏi broker (rc={rc})")

client = mqtt.Client(client_id="test_pub_01")

# Gán callback
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect
client.connect(broker, port, 60)

# Bắt buộc để trigger callback
client.loop_start()

# Publish
result = client.publish(topic, json.dumps(message))
result.wait_for_publish()

if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Message published to topic: {topic}")
else:
    print("❌ Publish failed")

# Dừng loop và disconnect
client.loop_stop()
client.disconnect()