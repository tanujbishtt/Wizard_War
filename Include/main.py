import cv2
import mediapipe as mp
import socket
import collections

# --- CONFIGURATION ---
UDP_IP = "127.0.0.1"
UDP_PORT_P1 = 9000
UDP_PORT_P2 = 9001
DEBOUNCE_FRAMES = 3

# --- SOCKET SETUP ---
sock_p1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_p2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- MEDIAPIPE SETUP ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- BUFFERS ---
p1_buffer = collections.deque(maxlen=DEBOUNCE_FRAMES)
p2_buffer = collections.deque(maxlen=DEBOUNCE_FRAMES)

def get_gesture(hand_landmarks, label):
    lms = hand_landmarks.landmark
    
    # Helper: Y increases downwards.
    def is_finger_up(tip, pip):
        return lms[tip].y < lms[pip].y

    # Fingers Status
    index_up = is_finger_up(8, 6)
    middle_up = is_finger_up(12, 10)
    ring_up = is_finger_up(16, 14)
    pinky_up = is_finger_up(20, 18)
    
    # Count fingers up (excluding thumb for now)
    fingers_up_count = sum([index_up, middle_up, ring_up, pinky_up])
    
    # --- THUMB LOGIC (Based on Hand Side) ---
    # For Left Hand: Thumb is on Right side (higher X) when palm open
    # For Right Hand: Thumb is on Left side (lower X) when palm open
    # This assumes Palm facing camera.
    thumb_tip_x = lms[4].x
    thumb_mcp_x = lms[2].x
    
    thumb_out = False
    if label == "Left": # Actual Left Hand
        thumb_out = thumb_tip_x > thumb_mcp_x # Pointing Right (Inner)
    else: # Right Hand
        thumb_out = thumb_tip_x < thumb_mcp_x # Pointing Left (Inner)

    # --- GESTURE MAPPING ---

    # 1. FIST (0 fingers) -> Attack 1
    if fingers_up_count == 0:
        return "attack_1"

    # 2. PEACE SIGN (Index + Middle) -> Jump
    if index_up and middle_up and not ring_up and not pinky_up:
        return "jump"

    # 3. OPEN PALM -> Attack 2
    if fingers_up_count >= 4:
        return "attack_2"

    # 4. INDEX POINTING -> Move
    if index_up and not middle_up and not ring_up and not pinky_up:
        # Determine direction based on Tip X vs Knuckle X
        tip_x = lms[8].x
        knuckle_x = lms[5].x
        
        # Simple logic: Left side of screen vs Right side of screen relative to hand
        if tip_x < knuckle_x:
            return "move_left" 
        else:
            return "move_right"

    return "idle"

def get_stable_action(buffer, new_action):
    buffer.append(new_action)
    if len(buffer) < DEBOUNCE_FRAMES:
        return "idle"
    counter = collections.Counter(buffer)
    if counter.most_common(1)[0][1] >= (DEBOUNCE_FRAMES - 1):
        return counter.most_common(1)[0][0]
    return buffer[-1]

print("Starting Controller...")
print("LEFT HAND = Player 1 | RIGHT HAND = Player 2")
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success: continue

    # Flip for mirror view
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    raw_p1 = "idle"
    raw_p2 = "idle"

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_lms in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            # Get Label: "Left" or "Right"
            # Note: MediaPipe labels are based on the hand itself.
            # In mirror mode (flip), "Left" usually means the user's Left hand.
            label = results.multi_handedness[idx].classification[0].label
            
            action = get_gesture(hand_lms, label)
            
            if label == "Left":
                raw_p1 = action
                cv2.putText(image, "P1 (Left)", (int(hand_lms.landmark[0].x * 640), int(hand_lms.landmark[0].y * 480)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                raw_p2 = action
                cv2.putText(image, "P2 (Right)", (int(hand_lms.landmark[0].x * 640), int(hand_lms.landmark[0].y * 480)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Stabilize and Send
    stable_p1 = get_stable_action(p1_buffer, raw_p1)
    stable_p2 = get_stable_action(p2_buffer, raw_p2)

    sock_p1.sendto(stable_p1.encode(), (UDP_IP, UDP_PORT_P1))
    sock_p2.sendto(stable_p2.encode(), (UDP_IP, UDP_PORT_P2))

    # UI
    cv2.putText(image, f"P1 Action: {stable_p1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, f"P2 Action: {stable_p2}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Gesture Controller', image)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()