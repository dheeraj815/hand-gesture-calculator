import cv2
import mediapipe as mp

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Tip landmark IDs for each finger
tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    lm_list = []  # Landmark list

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                # Convert normalized (0-1) coordinates to pixels
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Check which fingers are up
    fingers = []

    if lm_list:
        # Thumb (x-coord logic)
        if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
            fingers.append(1)  # Up
        else:
            fingers.append(0)  # Down

        # Other four fingers (y-coord logic)
        for i in range(1, 5):
            if lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Print the finger state
        print("Fingers up:", fingers)

        # Optional: Show number of fingers up
        cv2.putText(img, f'Fingers: {fingers.count(1)}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Step 3: Finger Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
gesture_map = {
    # other digits/operators here...
    (0, 0, 0, 0, 0): "=",  # equals as fist
    (0, 1, 0, 0, 0): "1",
    (0, 1, 1, 0, 0): "2",
    # etc.
}
