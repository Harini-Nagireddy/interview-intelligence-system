import cv2

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    total_frames = 0
    face_detected_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )

        if len(faces) > 0:
            face_detected_frames += 1

    cap.release()

    presence_percentage = (face_detected_frames / total_frames) * 100

    return {
        "total_frames": total_frames,
        "face_detected_frames": face_detected_frames,
        "camera_presence": round(presence_percentage, 2)
    }
