import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)  # Initialize for 1 hand

# Initialize video capture
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height
frameR = 100
smoothening = 8

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wscr, hscr = pyautogui.size()  # Get screen size

while True:
    success, img = cap.read()
    if not success:
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            lmList = [(lm.x * wCam, lm.y * hCam) for lm in handLms.landmark]

            if lmList:
                x1, y1 = int(lmList[8][0]), int(lmList[8][1])
                x2, y2 = int(lmList[12][0]), int(lmList[12][1])

                # Convert coordinates with interpolation
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wscr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hscr))

                # Smoothen values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                pyautogui.moveTo(wscr - clocX, clocY)
                plocX, plocY = clocX, clocY

                # Clicking mode
                length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if length < 40:
                    pyautogui.click()

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
