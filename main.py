import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Camera
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Screen size
wscr, hscr = pyautogui.size()

# Frame and smoothening
frameR = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Timers and thresholds
click_threshold = 40
click_delay = 0.3
last_click_time = 0
scroll_sensitivity = 15
zoom_sensitivity = 5

# Finger tips
tip_ids = [4, 8, 12, 16, 20]

pTime = 0

def fingers_up(lm_list):
    fingers = []

    # Thumb
    if lm_list[4][0] > lm_list[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        lm_list = []
        for id, lm in enumerate(handLms.landmark):
            cx, cy = int(lm.x * wCam), int(lm.y * hCam)
            lm_list.append((cx, cy))

        if lm_list:
            x1, y1 = lm_list[8]   # Index
            x2, y2 = lm_list[12]  # Middle
            x_thumb, y_thumb = lm_list[4]  # Thumb

            # Fingers up status
            fingers = fingers_up(lm_list)
            total_fingers = sum(fingers)

            # Mouse Movement - only index finger up
            if fingers[1] == 1 and total_fingers == 1:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wscr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hscr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                pyautogui.moveTo(wscr - clocX, clocY)
                plocX, plocY = clocX, clocY
                cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

            # Left Click - index + middle finger close together
            elif fingers[1] == 1 and fingers[2] == 1:
                length = math.hypot(x2 - x1, y2 - y1)
                if length < click_threshold and time.time() - last_click_time > click_delay:
                    pyautogui.click()
                    last_click_time = time.time()
                    cv2.circle(img, ((x1 + x2)//2, (y1 + y2)//2), 12, (0, 0, 255), cv2.FILLED)

            # Scroll - index and middle up, thumb down
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                scroll_dir = y2 - y1
                if abs(scroll_dir) > scroll_sensitivity:
                    pyautogui.scroll(-1 if scroll_dir > 0 else 1)
                    cv2.putText(img, "Scroll", (10, hCam - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Zoom - thumb and index pinch
            elif fingers[0] == 1 and fingers[1] == 1:
                zoom_distance = math.hypot(x1 - x_thumb, y1 - y_thumb)
                if zoom_distance < 40:
                    pyautogui.hotkey('ctrl', '-')  # Zoom out
                elif zoom_distance > 80:
                    pyautogui.hotkey('ctrl', '+')  # Zoom in
                cv2.putText(img, "Zoom", (10, hCam - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # Right click - three fingers up
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                if time.time() - last_click_time > click_delay:
                    pyautogui.click(button='right')
                    last_click_time = time.time()
                    cv2.putText(img, "Right Click", (10, hCam - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime + 1e-5)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display
    cv2.imshow("Virtual Mouse with Gestures", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
