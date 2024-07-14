# emotion_detection.py
from fer import FER
import cv2
import matplotlib.pyplot as plt
import numpy as np
import imageio
import matplotlib
import threading
import time

# Set the backend for matplotlib to 'Agg' for compatibility with different environments
matplotlib.use('Agg')

# Initialize the FER (Face Emotion Recognition) detector using MTCNN
detector = FER(mtcnn=True)

def detect_emotions_for_duration(duration, stop_event):
    cap = cv2.VideoCapture(0)
    frame_rate = 4.3
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('emotion_video.avi', fourcc, frame_rate, (640, 480))

    plt.ion()
    fig, ax = plt.subplots()
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    bars = ax.bar(emotion_labels, [0] * 7, color='lightblue')
    plt.ylim(0, 1)
    plt.ylabel('Confidence')
    plt.title('Real-time Emotion Detection')
    ax.set_xticks(range(len(emotion_labels)))  # 设置固定的刻度
    ax.set_xticklabels(emotion_labels, rotation=45)

    gif_writer = imageio.get_writer('emotion_chart.gif', mode='I', duration=0.1)
    emotion_statistics = {emotion: 0 for emotion in emotion_labels}

    def update_chart(detected_emotions):
        ax.clear()
        ax.bar(emotion_labels, [detected_emotions.get(emotion, 0) for emotion in emotion_labels], color='lightblue')
        plt.ylim(0, 1)
        plt.ylabel('Confidence')
        plt.title('Real-time Emotion Detection')
        ax.set_xticks(range(len(emotion_labels)))  # 设置固定的刻度
        ax.set_xticklabels(emotion_labels, rotation=45)
        fig.canvas.draw()
        fig.canvas.flush_events()

    start_time = time.time()

    try:
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.detect_emotions(frame)
            largest_face = None
            max_area = 0

            for face in result:
                box = face["box"]
                x, y, w, h = box
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_face = face

            if largest_face:
                box = largest_face["box"]
                current_emotions = largest_face["emotions"]

                for emotion, score in current_emotions.items():
                    emotion_statistics[emotion] += score

                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                emotion_type = max(current_emotions, key=current_emotions.get)
                emotion_score = current_emotions[emotion_type]

                emotion_text = f"{emotion_type}: {emotion_score:.2f}"
                cv2.putText(frame, emotion_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                update_chart(current_emotions)

                out.write(frame)

                fig.canvas.draw()
                image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                gif_writer.append_data(image)

            cv2.imshow('Emotion Detection', frame)
            if time.time() - start_time >= duration:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        plt.close(fig)

        out.release()
        gif_writer.close()

        final_emotion = max(emotion_statistics, key=emotion_statistics.get)
        final_score = emotion_statistics[final_emotion]

        with open('final_emotion.txt', 'w') as f:
            f.write(f"Final Emotion: {final_emotion}\n")
            f.write(f"Score: {final_score:.2f}\n")

def start_emotion_detection(duration=5, stop_event=None):
    if stop_event is None:
        stop_event = threading.Event()
    detection_thread = threading.Thread(target=detect_emotions_for_duration, args=(duration, stop_event))
    detection_thread.start()
    return stop_event