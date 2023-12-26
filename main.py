import cv2 
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
import time
import streamlit as st
import webbrowser
from directkeys import space_pressed

st.set_page_config(page_title="Dino Game with Hand Controller", page_icon="🤖")

def open_url(url):
    webbrowser.open_new_tab(url)

def main():
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    space_key_pressed = space_pressed
    time.sleep(2.0)
    current_key_pressed = set()

    st.title("Dino Game with Hand Controller")
    st.text("Now Click the Open Dino Game Button to Play ....")

    # Create a vertical sidebar
    st.sidebar.title("Controls")

    stop_button_pressed = st.sidebar.button("Stop")
    dino_game_button_pressed = st.sidebar.button("Open Dino Game")
    reload_button_pressed = st.sidebar.button("Restart the Controllers")

    # Define the URL you want to open
    url_to_open = "https://offline-dino-game.firebaseapp.com/"

    # Create a button in Streamlit
    if dino_game_button_pressed:
        # If the button is clicked, open the URL
        open_url(url_to_open)

    video_placeholder = st.empty()
    video = cv2.VideoCapture(0)

    hide_stremlit_styles = """
        <style>
        #MainMenu{visibility:hidden;}
        header{visibility:hidden;}
        footer{visibility:hidden;}
        </style>
    """
    st.markdown(hide_stremlit_styles,unsafe_allow_html=True)

    st.markdown('<hr><center><a href="https://www.instagram.com/suraj_nate/" target="_blank" style="color:white;text-decoration:none">@suraj_nate</a></center>', unsafe_allow_html=True)

    while True:
        ret, frame = video.read()

        keyPressed = False
        spacePressed = False
        key_count = 0
        key_pressed = 0

        hands, img = detector.findHands(frame)

        cv2.rectangle(img, (0, 480), (300, 425), (50, 50, 255), -2)
        cv2.rectangle(img, (640, 480), (400, 425), (50, 50, 255), -2)

        if hands:
            lmList = hands[0]
            fingerUp = detector.fingersUp(lmList)
            print(fingerUp)

            if fingerUp == [0, 0, 0, 0, 0]:
                cv2.putText(frame, 'Finger Count : 0', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Jumping', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(space_key_pressed)
                spacePressed = True
                current_key_pressed.add(space_key_pressed)
                key_pressed = space_key_pressed
                keyPressed = True
                key_count = key_count + 1

            if fingerUp == [0, 1, 0, 0, 0]:
                cv2.putText(frame, 'Finger Count : 1', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (415, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
            if fingerUp == [0, 1, 1, 0, 0]:
                cv2.putText(frame, 'Finger Count : 2', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (415, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
            if fingerUp == [0, 1, 1, 1, 0]:
                cv2.putText(frame, 'Finger Count : 3', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (415, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
            if fingerUp == [0, 1, 1, 1, 1]:
                cv2.putText(frame, 'Finger Count : 4', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (415, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
            if fingerUp == [1, 1, 1, 1, 1]:
                cv2.putText(frame, 'Finger Count : 5', (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (415, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
            elif key_count == 1 and len(current_key_pressed) == 2:
                for key in current_key_pressed:
                    if key_pressed != key:
                        ReleaseKey(key)
                current_key_pressed = set()

        video_placeholder.image(frame, channels="BGR")

        if stop_button_pressed:
            break

        if reload_button_pressed:
            # Reload the Streamlit app page
            st.experimental_rerun()

    video.release()
    

if __name__ == "__main__":
    main()
