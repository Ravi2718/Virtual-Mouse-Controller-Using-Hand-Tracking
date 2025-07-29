import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Initialize video capture
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Screen dimensions
wscr, hscr = pyautogui.size()

# Parameters
frameR = 100  # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
click_cooldown = 0.3
last_click_time = 0

# Finger tip landmarks
tip_ids = [4, 8, 12, 16, 20]

def fingers_up(lm_list):
    fingers = []

    # Thumb
    if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Flip for mirror view
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lm_list = []
    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
        for id, lm in enumerate(handLms.landmark):
            cx, cy = int(lm.x * wCam), int(lm.y * hCam)
            lm_list.append((cx, cy))

    if lm_list:
        x1, y1 = lm_list[8]  # Index tip
        x2, y2 = lm_list[12] # Middle tip

        fingers = fingers_up(lm_list)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        if fingers[1] == 1 and fingers[2] == 0:  # Moving Mode: Index up, middle down
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wscr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hscr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(wscr - clocX, clocY)
            plocX, plocY = clocX, clocY

            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

        if fingers[1] == 1 and fingers[2] == 1:  # Clicking Mode: Index and middle up
            length = math.hypot(x2 - x1, y2 - y1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            if length < 40 and (time.time() - last_click_time) > click_cooldown:
                pyautogui.click()
                last_click_time = time.time()
                cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 12, (0, 0, 255), cv2.FILLED)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if 'pTime' in locals() else 0
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Hand Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
