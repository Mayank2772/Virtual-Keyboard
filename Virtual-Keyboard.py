import cv2
import mediapipe as mp
import math
from time import sleep
from pynput.keyboard import Controller, Key

# Initialize the hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Setup screen capture
cap = cv2.VideoCapture(0)  # Try 0 if 1 doesn't work
cap.set(3, 1280)  # Width of video frame
cap.set(4, 720)   # Height of video frame

# Define keyboard layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "ENTER"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "DEL"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?", "CAPS"]]

finalText = ""
caps_lock = True  # Initialize Caps Lock state

# Initialize keyboard controller
keyboard = Controller()

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def drawALL(image, buttonList, highlightedButton=None, clickedButton=None):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        if button.text == "DEL":
            w += 90  
        if button.text == "CAPS":
            w += 100  
        if button.text == "ENTER":
            w += 120  

        if button == highlightedButton:
            cv2.rectangle(image, button.pos, (x + w, y + h), (175, 0, 175), -1)
        elif button == clickedButton:
            cv2.rectangle(image, button.pos, (x + w, y + h), (0, 255, 0), -1)
        else:
            cv2.rectangle(image, button.pos, (x + w, y + h), (255, 0, 255), -1)

        cv2.putText(image, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return image

# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create buttons
buttonList = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        x = 100 * j + 50
        y = 100 * i + 50
        buttonList.append(Button([x, y], key))

clickedButton = None
finger_press_count = 0
click_threshold = 50  # Distance threshold for click detection

while True:
    success, image = cap.read()
    
    # Check if the frame was captured successfully
    if not success or image is None:
        print("Failed to grab frame")
        continue

    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR2RGB for MediaPipe
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # RGB2BGR for OpenCV display

    highlightedButton = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = (int(hand_landmarks.landmark[8].x * image.shape[1]),
                                int(hand_landmarks.landmark[8].y * image.shape[0]))
            middle_finger_tip = (int(hand_landmarks.landmark[12].x * image.shape[1]),
                                 int(hand_landmarks.landmark[12].y * image.shape[0]))

            distance = calculate_distance(index_finger_tip, middle_finger_tip)

            for button in buttonList:
                bx, by = button.pos
                bw, bh = button.size

                if bx < index_finger_tip[0] < bx + bw and by < index_finger_tip[1] < by + bh:
                    highlightedButton = button

                    if distance < click_threshold:
                        finger_press_count += 1
                        if finger_press_count == 2:
                            clickedButton = button
                            if button.text == "DEL":
                                keyboard.press(Key.backspace)
                                keyboard.release(Key.backspace)
                                finalText = finalText[:-1]
                            elif button.text == "CAPS":
                                caps_lock = not caps_lock
                            elif button.text == "ENTER":
                                keyboard.press(Key.enter)
                                keyboard.release(Key.enter)
                                finalText = ""
                            else:
                                char = button.text.upper() if caps_lock else button.text.lower()
                                keyboard.press(char)
                                finalText += char
                            sleep(0.20)
                            cv2.waitKey(1)
                            finger_press_count = 0
                            break
                    else:
                        finger_press_count = 0

    # Draw text box
    cv2.rectangle(image, (50, 400), (1250, 500), (255, 0, 255), -1)
    cv2.putText(image, finalText, (60, 475), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    image = drawALL(image, buttonList, highlightedButton, clickedButton)

    cv2.imshow('Hand Detection', image)
    key = cv2.waitKey(1)
    if key & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
