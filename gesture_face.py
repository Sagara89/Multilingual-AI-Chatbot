import cv2
import mediapipe as mp
from collections import Counter

# ---------------- INIT ----------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

mp_draw = mp.solutions.drawing_utils

# ---------------- DETECT GESTURE ----------------
def detect_gesture():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Camera Error"

    gesture_history = []

    while True:

        success, img = cap.read()

        if not success:
            break

        img = cv2.flip(img, 1)

        img_rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(img_rgb)

        gesture = "Unknown"

        # ---------------- HAND DETECTION ----------------
        if results.multi_hand_landmarks and results.multi_handedness:

            for handLms, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                mp_draw.draw_landmarks(
                    img,
                    handLms,
                    mp_hands.HAND_CONNECTIONS
                )

                lm = handLms.landmark

                label = handedness.classification[0].label

                fingers = []

                # ---------------- THUMB ----------------
                if label == "Right":

                    fingers.append(
                        1 if lm[4].x < lm[3].x - 0.02 else 0
                    )

                else:

                    fingers.append(
                        1 if lm[4].x > lm[3].x + 0.02 else 0
                    )

                # ---------------- OTHER FINGERS ----------------
                tips = [8, 12, 16, 20]
                pips = [6, 10, 14, 18]

                for tip, pip in zip(tips, pips):

                    fingers.append(
                        1 if lm[tip].y < lm[pip].y - 0.02 else 0
                    )

                # ---------------- GESTURE LOGIC ----------------

                # ✋ Hello
                if fingers == [1,1,1,1,1]:
                    gesture = "Hello"

                # 🖐 Stop
                elif fingers == [0,1,1,1,1]:
                    gesture = "Stop"

                # ✌ Peace
                elif fingers == [0,1,1,0,0]:
                    gesture = "Peace"

                # ☝ Help
                elif fingers == [0,1,0,0,0]:
                    gesture = "Help"

                # 👍 Good
                elif fingers == [1,0,0,0,0]:
                    gesture = "Good"

                # 🤙 Call Me
                elif fingers == [1,0,0,0,1]:
                    gesture = "Call Me"

                # 🤟 I Love You
                elif fingers == [1,1,0,0,1]:
                    gesture = "I Love You"

                # 👉 Pointing
                elif fingers == [1,1,0,0,0]:
                    gesture = "Pointing"

                # ✊ Closed Hand
                elif fingers == [0,0,0,0,0]:

                    # Thumb inside = No
                    is_tucked = (
                        (label == "Right" and lm[4].x > lm[5].x)
                        or
                        (label == "Left" and lm[4].x < lm[5].x)
                    )

                    if is_tucked:
                        gesture = "No"
                    else:
                        gesture = "Yes"

        # ---------------- STABILITY FILTER ----------------
        if gesture != "Unknown":

            gesture_history.append(gesture)

        if len(gesture_history) > 10:

            gesture_history.pop(0)

        if gesture_history:

            final = Counter(
                gesture_history
            ).most_common(1)[0][0]

        else:
            final = "Unknown"

        # ---------------- DISPLAY ----------------
        cv2.putText(
            img,
            f"Gesture: {final}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            img,
            "Press ESC to Confirm",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        cv2.imshow("Gesture Detection", img)

        # ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

    cv2.destroyAllWindows()

    return final