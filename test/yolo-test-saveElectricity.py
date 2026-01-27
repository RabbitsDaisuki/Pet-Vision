"""
Pure Software Power-Saving YOLO System
- No PIR sensor required
- Motion-based detection
- Safe exit & resource cleanup
Python 3.11
"""

from ultralytics import YOLO
import cv2
import time
import sys
import select

# =============================
# 1️⃣ 系統設定
# =============================

MODEL_PATH = "yolov8n.pt"

TARGET_CLASSES = ["person", "dog", "cat", "bird"]

YOLO_IMG_SIZE = 320
YOLO_CONF = 0.4

# 每幾幀最多跑一次 YOLO（上限保護）
YOLO_INTERVAL = 20

# 畫面變化門檻（越大越不敏感）
MOTION_THRESHOLD = 25_000

# 偵測後維持顯示多久（秒）
DISPLAY_HOLD_TIME = 2.0


# =============================
# 2️⃣ 初始化
# =============================

print("[INFO] Loading YOLO model...")
model = YOLO(MODEL_PATH)

print("[INFO] Opening camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Camera not available")
    sys.exit(1)

prev_gray = None
frame_count = 0

last_results = None
last_detect_time = 0

print("[INFO] System running (press 'q' to quit)")


# =============================
# 3️⃣ 主迴圈
# =============================

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        now = time.time()

        # -------------------------
        # 3-1 畫面變化偵測（超省電）
        # -------------------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        motion_score = 0
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            motion_score = diff.sum()

        prev_gray = gray

        run_yolo = False

        # 畫面有明顯變化，且符合 interval 才跑 YOLO
        if motion_score > MOTION_THRESHOLD:
            if frame_count % YOLO_INTERVAL == 0:
                run_yolo = True

        # -------------------------
        # 3-2 YOLO 推論
        # -------------------------
        if run_yolo:
            last_results = model(
                frame,
                imgsz=YOLO_IMG_SIZE,
                conf=YOLO_CONF,
                verbose=False
            )

            if last_results and len(last_results[0].boxes) > 0:
                last_detect_time = now

        # -------------------------
        # 3-3 顯示結果（使用快取）
        # -------------------------
        if last_results and (now - last_detect_time < DISPLAY_HOLD_TIME):
            for box in last_results[0].boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                if label not in TARGET_CLASSES:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 255, 0), 2)
                cv2.putText(frame, label.upper(),
                            (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)

        # -------------------------
        # 3-4 顯示畫面
        # -------------------------
        cv2.imshow("YOLO Power-Saving Mode", frame)

        # OpenCV 視窗按 q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Quit from window")
            break

        # Terminal 輸入 q（不用 Enter）
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            if key.lower() == 'q':
                print("[INFO] Quit from terminal")
                break


except KeyboardInterrupt:
    print("\n[INFO] Keyboard interrupt")

finally:
    # =============================
    # 4️⃣ 資源釋放（產品級）
    # =============================
    print("[INFO] Releasing resources...")
    cap.release()
    cv2.destroyAllWindows()
    del model
    print("[INFO] System shutdown complete")
