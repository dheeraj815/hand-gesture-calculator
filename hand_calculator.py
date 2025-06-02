import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam capture
cap = cv2.VideoCapture(0)

# Gesture map: (Thumb, Index, Middle, Ring, Pinky)
gesture_map = {
    (0, 1, 0, 0, 0): "1",
    (0, 1, 1, 0, 0): "2",
    (0, 1, 1, 1, 0): "3",
    (0, 1, 1, 1, 1): "4",
    (1, 1, 1, 1, 1): "5",
    (1, 1, 0, 0, 0): "+",
    (1, 0, 0, 0, 0): "-",
    (1, 1, 1, 0, 0): "*",
    (0, 0, 0, 0, 0): "=",  # Equals gesture as fist (all fingers down)
    (1, 0, 0, 0, 1): "C"   # Clear gesture (thumb and pinky up)
}

equation = ""
result = ""
last_gesture = None
delay_counter = 0
delay_threshold = 20  # frames to wait before accepting new gesture


def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # Other fingers
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return tuple(fingers)


while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result_hands = hands.process(img_rgb)

    if result_hands.multi_hand_landmarks:
        hand_landmarks = result_hands.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        finger_tuple = fingers_up(hand_landmarks)
        cv2.putText(img, f"Fingers: {finger_tuple}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if delay_counter == 0:
            if finger_tuple in gesture_map:
                gesture = gesture_map[finger_tuple]
                if gesture != last_gesture:
                    if gesture == "C":
                        equation = ""
                        result = ""
                    elif gesture == "=":
                        try:
                            # Evaluate the expression safely
                            result = str(eval(equation))
                        except:
                            result = "Error"
                        equation = ""
                    else:
                        equation += gesture
                    last_gesture = gesture
                    delay_counter = delay_threshold
        else:
            delay_counter -= 1
    else:
        last_gesture = None

    # Show current equation
    cv2.putText(img, f"Expr: {equation}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Show result if available
    if result != "":
        cv2.putText(img, f"Result: {result}", (10, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Hand Gesture Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
