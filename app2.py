import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import random
from ultralytics import YOLO
import torch
import cv2
import av
# import time
import numpy as np
import threading
import queue
from typing import List, NamedTuple
import logging
from resources import word_list

# streamlit-webrtc:
#  real-time video/audio streams over the network with Streamlit
#  See more at https://github.com/whitphx/streamlit-webrtc

class Detection(NamedTuple):
    label: str
    conf: float
    box: np.ndarray


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
recognizer = YOLO('./muhammad.pt')
recognizer.to(device)

logger = logging.getLogger(__name__)

st.title('Wordle Game with ASL Fingerspelling')
flip = st.checkbox("Flip")
confidence_threshold = st.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.05)

result_queue: "queue.Queue[List[Detection]]" = queue.Queue()


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    image = image[:, ::-1, :] if flip else image

    best_result = None
    max_conf = 0.0

    # Run recognizer
    # type: ultralytics.engine.results.BaseTensor
    results = recognizer(image, conf=confidence_threshold)

    # Render bounding boxes and captions
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy(),
        confs = result.boxes.conf.cpu().numpy(),
        labels = result.boxes.cls.cpu().numpy(),
        image_copy = image.copy()

        if len(confs) == 0:
            continue

        # Find the index of the highest confidence
        max_conf_index = np.argmax(confs)
        max_conf = confs[max_conf_index]

        if max_conf < confidence_threshold:
            continue

        box = boxes[max_conf_index]
        label = labels[max_conf_index]

    #     best_result = (box, max_conf, label)

    # #     # result_queue.put()

    print('hello!!!!!!!!!')
    print(box)

    cv2.rectangle(
        image_copy,
        (int(box[0]), int(box[1])),
        (int(box[2]), int(box[3])),
        (0, 255, 0), 2
    )
    cv2.putText(
        image_copy,
        f"{recognizer.names[int(label)]} ({max_conf:.2f})",
        (int(box[0]), int(box[1] - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2
    )

    # if best_result is not None:
    #     print(best_result)
    #     _, _, label = best_result
        
    #     # recognizer.names[int(label)], max_conf, 
    #     frame = av.VideoFrame.from_ndarray(image, format="bgr24")
    #     return frame

    # "", 0.0
    frame = av.VideoFrame.from_ndarray(image, format="bgr24")
    return frame


webrtc_streamer(
    key="object-detection",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)

# if st.checkbox("Show the detected alphabets", value=True):
#     if webrtc_ctx.state.playing:
#         labels_placeholder = st.empty()
#         while True:
#             result = result_queue.get()
#             labels_placeholder.table(result)

# if st.checkbox("Show the detected labels", value=True):
#     if webrtc_ctx.state.playing:
#         labels_placeholder = st.empty()
#         while True:
#             result = result_queue.get()
#             labels_placeholder.table(result)

# ======================================================

# if 'target_word' in st.session_state:
#     target_word = st.session_state.target_word
# else:
#     target_word = random.choice(word_list)
# st.session_state['target_word'] = target_word
# st.write(f"Your target word is {target_word.upper()} for testing purposes.")

# def start_recording() -> str:
#     """Start recording from the camera and recognize gestures continuously. \
# This function handles camera streaming and calls recognize_and_draw \
# to process each frame.

#     Returns:
#     str: The sequence of recognized letters as a string.
#     """
#     global recording
#     recording = True
#     frame_buffer = []
#     while recording:
#         ret, frame = camera.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             letter, _, frame_with_box = recognize_and_draw(frame)
#             FRAME_WINDOW.image(frame_with_box, use_column_width=True)
#             frame_buffer.append(letter)
#             time.sleep(0.05)
#     return ''.join(frame_buffer[:5])


# def stop_recording():
#     """Stop the recording and release the camera."""
#     global recording, camera
#     recording = False
#     if camera.isOpened():
#         camera.release()
#         st.write("Camera released")


# start_button = st.button('Start Recording' if not recording
#                          else 'Stop Recording'
#                          )
# if start_button:
#     if not recording:
#         guessed_word = start_recording()
#         st.write(f"Recognized letters: {guessed_word.upper()}")
#     else:
#         stop_recording()
