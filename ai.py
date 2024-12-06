from flask import Flask, render_template, jsonify
import mediapipe as mp
import cv2
import time

app = Flask(__name__)

# ตัวแปรสำหรับส่งข้อมูลจำนวนของนิ้ว
num_fingers = 0

# ฟังก์ชั่นในการตรวจจับนิ้ว
def count_fingers():
    global num_fingers
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                fingers = []
                if handLms.landmark[4].x < handLms.landmark[3].x:  # นิ้วโป้ง
                    fingers.append(1)
                else:
                    fingers.append(0)

                if handLms.landmark[8].y < handLms.landmark[6].y:  # นิ้วชี้
                    fingers.append(1)
                else:
                    fingers.append(0)

                if handLms.landmark[12].y < handLms.landmark[10].y:  # นิ้วกลาง
                    fingers.append(1)
                else:
                    fingers.append(0)

                if handLms.landmark[16].y < handLms.landmark[14].y:  # นิ้วนาง
                    fingers.append(1)
                else:
                    fingers.append(0)

                if handLms.landmark[20].y < handLms.landmark[18].y:  # นิ้วก้อย
                    fingers.append(1)
                else:
                    fingers.append(0)

                num_fingers = sum(fingers)  # คำนวณจำนวนของนิ้วที่ยกขึ้น

        time.sleep(1)  # รอ 1 วินาทีเพื่อให้การตรวจจับไม่เกินความสามารถ
        cap.release()

# ตั้งให้ Flask ให้เปิด server เมื่อเริ่มใช้งาน
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_fingers')
def get_fingers():
    return jsonify({'fingers': num_fingers})

if __name__ == '__main__':
    # เริ่มทำงานใน Thread แยก
    import threading
    threading.Thread(target=count_fingers).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
