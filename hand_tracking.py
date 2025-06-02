import cv2
import mediapipe as mp

# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,                 # We'll use only one hand for calculator input
    min_detection_confidence=0.7,    # Confidence threshold for detection
    min_tracking_confidence=0.7      # Confidence threshold for tracking
)

# Drawing utility
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Main loop
while True:
    success, img = cap.read()  # Capture frame
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    results = hands.process(img_rgb)

    # Draw landmarks if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)

    # Display the image
    cv2.imshow("Step 2: Hand Tracking", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
print("Fingers detected:", finger_tuple)  # Show which fingers are up
if finger_tuple in gesture_map:
    gesture = gesture_map[finger_tuple]
    print("Gesture detected:", gesture)
