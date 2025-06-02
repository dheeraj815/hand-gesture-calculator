import cv2
import mediapipe as mp

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Finger tip landmark IDs
tip_ids = [4, 8, 12, 16, 20]

# Webcam
cap = cv2.VideoCapture(0)

# Gesture map
gesture_map = {
    (0, 1, 0, 0, 0): "1",
    (0, 1, 1, 0, 0): "2",
    (0, 1, 1, 1, 0): "3",
    (0, 1, 1, 1, 1): "4",
    (1, 1, 1, 1, 1): "5",
    (1, 0, 0, 0, 1): "+",
    (1, 1, 0, 0, 0): "-",
    (1, 0, 0, 1, 1): "*",
    (0, 0, 0, 0, 0): "C"
}

# Store the last gesture
last_gesture = None
gesture_delay = 20
delay_counter = 0

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    lm_list = []

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))
            mp_draw.draw_landmarks(
                img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Detect finger states
    fingers = []

    if lm_list:
        # Thumb (horizontal)
        fingers.append(1 if lm_list[4][1] > lm_list[3][1] else 0)

        # Other 4 fingers (vertical)
        for i in range(1, 5):
            fingers.append(1 if lm_list[tip_ids[i]]
                           [2] < lm_list[tip_ids[i] - 2][2] else 0)

        finger_tuple = tuple(fingers)

        # Gesture recognition with delay to avoid rapid flickering
        if delay_counter == 0:
            if finger_tuple in gesture_map:
                gesture = gesture_map[finger_tuple]
                if gesture != last_gesture:
                    print("Gesture:", gesture)
                    last_gesture = gesture
                    delay_counter = gesture_delay

        else:
            delay_counter -= 1

        # Draw recognized gesture
        if last_gesture:
            cv2.putText(img, f"Gesture: {last_gesture}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Step 4: Gesture Mapping", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if gesture == "=":
    print("Evaluating equation:", equation)
    try:
        result = str(eval(equation))
    except Exception as e:
        print("Error:", e)
        result = "Error"
    equation = ""
