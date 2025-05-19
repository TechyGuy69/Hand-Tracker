import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to recognize hand gesture (just an example for play/pause gesture)
def recognize_gesture(hand_landmarks):
    # You can define gestures based on landmarks
    # For simplicity, I'm using the distance between thumb and index finger as an example
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    # Calculate the distance between thumb and index finger
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    
    # Gesture control based on distance (example: smaller distance = play/pause gesture)
    if distance < 0.05:
        return "play_pause"  # Gesture for play/pause
    else:
        return None  # No gesture detected

# Function to control media playback (play/pause)
def control_media_playback(gesture):
    if gesture == "play_pause":
        pyautogui.press('playpause')  # Simulate pressing the play/pause key

# Start capturing from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture image")
        break
    
    # Flip the frame for a better user experience (optional)
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and find hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Recognize the gesture based on hand landmarks
            gesture = recognize_gesture(hand_landmarks)
            if gesture:
                print(f"Detected gesture: {gesture}")
                control_media_playback(gesture)  # Perform media control action
    
    # Show the frame
    cv2.imshow("Hand Gesture Control", frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
