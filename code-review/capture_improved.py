from serial import Serial
import cv2
import datetime

ser = Serial('COM7', 9600)
video_device_index = 1

# 分状态报错，便于检修
ERR_CAMERA_OPEN   = "E01: 摄像头无法打开（检查USB连接/占用）"
ERR_CAMERA_READ   = "E02: 摄像头已打开但抓帧失败"
ERR_SERIAL_FORMAT = "E03: 收到无法识别的串口数据"

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()

        if data != 'Entry detected':
            print(ERR_SERIAL_FORMAT, f"收到: {data}")   # 未知消息也报，便于排查
            continue

        # 打开摄像头(先检查，再继续)
        capture = cv2.VideoCapture(video_device_index)
        if not capture.isOpened():
            print(ERR_CAMERA_OPEN)
            continue                                     # 本次放弃，等下一辆车，不崩程序

        time.sleep(4)
        ret, frame = capture.read()
        if not ret:                                      # 打开成功但拍不到也单独报
            print(ERR_CAMERA_READ)
            capture.release()
            continue

        # 启用时间戳文件名，不覆盖历史照片
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        capture.release()
        print(f"OK: {filename}")