#!/usr/bin/env python3
"""
TestLoaDenCoi_IOT - MQTT Publisher for IoT Horn / Siren Speaker (MGSP-V1)

Sends command payload via MQTT to trigger audio playback from an HTTP stream URL.
Supports configuration via command-line arguments and environment variables.
"""

import os
import sys
import json
import argparse
import paho.mqtt.client as mqtt


def parse_args():
    parser = argparse.ArgumentParser(
        description="MQTT Publisher for IoT Horn/Siren Speaker (MGSP-V1)"
    )
    parser.add_argument(
        "--broker",
        default=os.getenv("MQTT_BROKER", "45.117.170.179"),
        help="MQTT broker host/IP (default: 45.117.170.179 or $MQTT_BROKER)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MQTT_PORT", "1883")),
        help="MQTT broker port (default: 1883 or $MQTT_PORT)",
    )
    parser.add_argument(
        "--topic",
        default=os.getenv("MQTT_TOPIC", "MGSP-V1/F055CF453AB4/cmd"),
        help="MQTT topic (default: MGSP-V1/F055CF453AB4/cmd or $MQTT_TOPIC)",
    )
    parser.add_argument(
        "--url",
        default=os.getenv("AUDIO_STREAM_URL", "http://192.168.10.4:8090/2.mp3"),
        help="Audio stream URL (default: http://192.168.10.4:8090/2.mp3 or $AUDIO_STREAM_URL)",
    )
    parser.add_argument(
        "--request-id",
        default=os.getenv("REQUEST_ID", "999"),
        help="Request ID for tracking (default: 999 or $REQUEST_ID)",
    )
    parser.add_argument(
        "--client-id",
        default=os.getenv("MQTT_CLIENT_ID", "test_pub_01"),
        help="MQTT client ID (default: test_pub_01 or $MQTT_CLIENT_ID)",
    )
    return parser.parse_args()


# ===== Callbacks =====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Kết nối MQTT broker thành công")
    else:
        print(f"❌ Kết nối thất bại, mã lỗi: {rc}")


def on_disconnect(client, userdata, rc):
    print(f"⚠️ Đã disconnect khỏi broker (rc={rc})")


def main():
    args = parse_args()

    message = {
        "request_id": args.request_id,
        "audio_stream": {
            "url": args.url
        }
    }

    print(f"📡 Broker:    {args.broker}:{args.port}")
    print(f"📬 Topic:     {args.topic}")
    print(f"🎵 Audio URL: {args.url}")
    print(f"🆔 Req ID:    {args.request_id}")

    # Compatible with both paho-mqtt v1 and v2
    try:
        from paho.mqtt.enums import CallbackAPIVersion
        client = mqtt.Client(CallbackAPIVersion.VERSION1, client_id=args.client_id)
    except (ImportError, AttributeError):
        client = mqtt.Client(client_id=args.client_id)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect(args.broker, args.port, keepalive=60)
    except Exception as e:
        print(f"❌ Không thể kết nối tới broker: {e}")
        sys.exit(1)

    client.loop_start()

    payload_str = json.dumps(message, indent=2)
    print(f"📦 Payload gửi đi:\n{payload_str}")

    result = client.publish(args.topic, json.dumps(message))
    result.wait_for_publish()

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✅ Message published to topic: {args.topic}")
    else:
        print(f"❌ Publish failed with rc: {result.rc}")

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
