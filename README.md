# TestLoaDenCoi_IOT

Dự án Python thử nghiệm và điều khiển thiết bị loa / đèn còi thông minh IoT (model **MGSP-V1**) thông qua giao thức **MQTT**.

Hệ thống gửi gói tin lệnh JSON tới MQTT broker để thiết bị loa nhận lệnh, kết nối tới luồng HTTP audio và phát âm thanh cảnh báo hoặc thông báo.

---

## 📌 Cơ chế hoạt động

```
┌──────────────────┐     MQTT Publish      ┌──────────────────┐
│                  │  ──────────────────►  │                  │
│ Python Publisher │                       │   MQTT Broker    │
│    (code.py)     │  Topic:               │ (vd: Port 1883)  │
└──────────────────┘  MGSP-V1/{MAC}/cmd    └─────────┬────────┘
                                                     │
                                                     │ MQTT Subscribe
                                                     ▼
┌──────────────────┐    Tải & phát audio   ┌──────────────────┐
│   Audio Server   │  ◄──────────────────  │  Loa / Đèn Còi   │
│  (HTTP / MP3)    │                       │  IoT (MGSP-V1)   │
└──────────────────┘                       └──────────────────┘
```

---

## 📦 Cấu trúc Payload điều khiển

Gói tin điều khiển được đóng gói dạng JSON:

```json
{
  "request_id": "999",
  "audio_stream": {
    "url": "http://192.168.10.4:8090/2.mp3"
  }
}
```

- **`request_id`**: Mã định danh yêu cầu, dùng để theo dõi phiên điều khiển.
- **`audio_stream.url`**: Địa chỉ URL trực tiếp của luồng hoặc file âm thanh (MP3/WAV) mà loa IoT sẽ truy cập để phát.

---

## 🛠 Cài đặt

### Yêu cầu
- Python 3.8+
- Thư viện `paho-mqtt`

```bash
pip install -r requirements.txt
```

---

## 🚀 Hướng dẫn sử dụng

### 1. Chạy với thông số mặc định
```bash
python code.py
```

### 2. Chạy với đối số dòng lệnh (CLI flags)
```bash
python code.py \
  --broker 45.117.170.179 \
  --port 1883 \
  --topic "MGSP-V1/F055CF453AB4/cmd" \
  --url "http://192.168.10.4:8090/2.mp3" \
  --request-id "1001"
```

### 3. Cấu hình qua biến môi trường
```bash
export MQTT_BROKER="45.117.170.179"
export MQTT_PORT=1883
export MQTT_TOPIC="MGSP-V1/F055CF453AB4/cmd"
export AUDIO_STREAM_URL="http://192.168.10.4:8090/alert.mp3"
export REQUEST_ID="1002"

python code.py
```

---

## ⚙️ Bảng thông số cấu hình

| Tham số CLI | Biến môi trường | Mặc định | Mô tả |
|---|---|---|---|
| `--broker` | `MQTT_BROKER` | `45.117.170.179` | Địa chỉ IP hoặc hostname của MQTT Broker |
| `--port` | `MQTT_PORT` | `1883` | Cổng dịch vụ MQTT Broker |
| `--topic` | `MQTT_TOPIC` | `MGSP-V1/F055CF453AB4/cmd` | Topic điều khiển thiết bị (thay `F055CF453AB4` bằng MAC thiết bị) |
| `--url` | `AUDIO_STREAM_URL` | `http://192.168.10.4:8090/2.mp3` | Đường dẫn HTTP của file âm thanh cần phát |
| `--request-id` | `REQUEST_ID` | `999` | Mã theo dõi request |
| `--client-id` | `MQTT_CLIENT_ID` | `test_pub_01` | Client ID kết nối tới MQTT Broker |

---

## 📁 Cấu trúc thư mục

```
TestLoaDenCoi_IOT/
├── code.py           # Script chính gửi lệnh MQTT
├── Code.ipynb        # Jupyter Notebook thử nghiệm tương tác
├── requirements.txt  # Danh sách thư viện phụ thuộc
├── .gitignore        # Quy tắc loại trừ tệp
├── LICENSE           # Giấy phép nguồn mở MIT
└── README.md         # Tài liệu dự án
```

---

## 🔍 Xử lý sự cố (Troubleshooting)

1. **Lỗi kết nối MQTT (`Kết nối thất bại` / Timeout):**
   - Kiểm tra mạng và khả năng ping tới IP broker: `ping 45.117.170.179`.
   - Kiểm tra tường lửa / port 1883 có mở hay không: `nc -zv 45.117.170.179 1883` hoặc `telnet 45.117.170.179 1883`.

2. **Publish thành công nhưng loa không phát:**
   - Đảm bảo thiết bị loa IoT đang bật nguồn, kết nối mạng và đã subscribe đúng topic `MGSP-V1/{MAC}/cmd` (kiểm tra lại địa chỉ MAC của loa).
   - Kiểm tra URL âm thanh: Thiết bị loa phải truy cập được địa chỉ IP và port của audio server từ mạng nội bộ của nó.
   - Định dạng âm thanh: Khuyến nghị sử dụng chuẩn định dạng MP3 hoặc WAV với bitrate tiêu chuẩn.

---

## 📝 License

Dự án được phân phối dưới giấy phép **MIT**. Xem chi tiết tại tệp [LICENSE](LICENSE).
