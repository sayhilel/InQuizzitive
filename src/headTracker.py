import cv2
import random
import time
import textwrap
import numpy as np
from src.trivia_handler import qnaMap, wrongOptMap

#Resoultion option
resWidth = 800
resHeight = 600

#Video device
vDevice = 0

# Function to highlight text in an image
def highlight_text(image, text, org, font_face, font_scale, text_color, block_color, thickness):

    highlighted_image = image.copy()

    (text_width, text_height), baseline = cv2.getTextSize(text, font_face, font_scale, thickness)
    x1, y1 = org
    x2, y2 = x1 + text_width, y1 - text_height

    cv2.rectangle(highlighted_image, (x1, y1), (x2, y2), block_color, cv2.FILLED)

    cv2.putText(highlighted_image, text, org, font_face, font_scale, text_color, thickness)

    return highlighted_image

# Constants for colors
MAROON = (64, 29, 140)
WHITE = (255, 255, 255)
GOLD = (39, 198, 255)

# Class to represent answer options
class Option:
    def __init__(self, text, is_correct):
        self.text = text
        self.is_correct = is_correct

# Class to represent a question and its options
class Question:
    def __init__(self, question, option1, option2):

        self.question = question
        self.option1 = option1
        self.option2 = option2

# Function to check if two bounding boxes overlap
def check_overlap(box1, box2):

    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

# Main game function
def head_tracking_game():
    # Choose questions
    questions = []

    for question_text, correct_answer in qnaMap.items():
        wrong_answer = wrongOptMap[question_text]
        options = [Option(correct_answer, True), Option(wrong_answer, False)]
        random.shuffle(options)
        questions.append(Question(question_text, options[0], options[1]))

    # Video capture setup
    cap = cv2.VideoCapture(vDevice)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resHeight)
    cap.set(cv2.CAP_PROP_FPS, 60)  # Frame rate

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Timer, options, and score initialization
    next_question_time = None
    choice_time = None
    score = 0
    left_text_color = GOLD
    right_text_color = GOLD

    # Randomly select a question
    current_question = random.choice(questions)
    options = [current_question.option1, current_question.option2]
    random.shuffle(options)
    left_option, right_option = options
    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Mirror the video feed
        frame = cv2.flip(frame, 1)

        # Resize the frame
        height, width, _ = frame.shape
        scale_factor = 1.5
        frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
        height, width, _ = frame.shape

        # Define regions for left and right answer boxes
        quarter_width = width // 4
        left_box = (0, 0, quarter_width, height)
        right_box = (3 * quarter_width, 0, quarter_width, height)

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using Haar cascade
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        # Process each detected face
        for (x, y, w, h) in faces:
            # Display the current score near the detected face
            cv2.putText(frame, str(score), (x + w // 2, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check for overlap with left box
            if check_overlap((x, y, w, h), left_box):
                if choice_time is None:
                    choice_time = time.time()
                    if left_option.is_correct:
                        left_text_color = (0, 255, 0)  # Green
                        score += 1
                    else:
                        left_text_color = (0, 0, 255)  # Red
                        score -= 1

            # Check for overlap with right box
            if check_overlap((x, y, w, h), right_box):
                if choice_time is None:
                    choice_time = time.time()
                    if right_option.is_correct:
                        right_text_color = (0, 255, 0)  # Green
                        score += 1
                    else:
                        right_text_color = (0, 0, 255)  # Red
                        score -= 1

            # Process only one face (break out of the loop)
            break

        # Handle timing for next question
        if choice_time and time.time() < choice_time + 3:
            next_question_time = choice_time + 3

        # Check if it's time to display the next question
        if next_question_time and time.time() > next_question_time:
            # Reset timers and colors
            next_question_time = None
            choice_time = None
            left_text_color = GOLD
            right_text_color = GOLD

            # Randomly select a new question
            current_question = random.choice(questions)
            options = [current_question.option1, current_question.option2]
            random.shuffle(options)
            left_option, right_option = options

        # Wrap text for display
        wrapped_question = textwrap.wrap(current_question.question, width=22)
        wrapped_left_option = textwrap.wrap(left_option.text, width=32)
        wrapped_right_option = textwrap.wrap(right_option.text, width=22)

        # Text rendering parameters
        line_height = 30
        y_position = 50

        # Centering
        center_x = width // 2

        # Render wrapped question text
        for line in wrapped_question:
            text_width, text_height = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)[0]
            x_position = center_x - (text_width // 2)
            cv2.putText(frame, line, (x_position, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.75, MAROON, 2)
            y_position += line_height

        # Reset y position for options
        y_position = 50

        # Render wrapped left option text with highlighting
        for line in wrapped_left_option:
            frame = highlight_text(frame, line, (left_box[0] + 10, left_box[1] + y_position),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, left_text_color, (0, 0, 0), 2)
            y_position += line_height

        # Reset y position for options
        y_position = 50

        # Render wrapped right option text with highlighting
        for line in wrapped_right_option:
            frame = highlight_text(frame, line, (right_box[0] + 10, right_box[1] + y_position),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, right_text_color, (0, 0, 0), 2)
            y_position += line_height + 10

        # Encode the frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield frame_bytes

    # Release the video capture
    cap.release()
