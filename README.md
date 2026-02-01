🎤 Interview Intelligence System

An AI-powered system that analyzes a candidate’s mock interview performance using video and audio analysis. The system evaluates communication skills, confidence, and presentation quality and generates an automated performance report.

🚀 Features

🎥 Video Analysis – Detects face presence and measures camera engagement

🎙 Audio Analysis – Detects speech vs silence and evaluates speech pace

📝 Speech & Language Analysis – Word count, filler words, and speech structure

📊 Performance Scoring – Confidence, communication clarity, camera presence

📄 Automated Report Generation – Structured interview evaluation report

🖥 Live Mock Interview Mode – Records candidate using webcam and simulates a real interview

🛠 Tech Stack

Python • OpenCV • Vosk Speech Recognition • NLP • Streamlit

📂 Project Structure

Interview-Intelligence-System
│
├── app.py (Streamlit application)
├── camera_test.py (Webcam test)
├── requirements.txt (Dependencies)
│
├── modules/
│ ├── video_analysis.py
│ ├── audio_analysis.py
│ ├── speech_analysis.py
│ ├── scoring.py
│ └── report_generator.py

⚙️ Setup Instructions
1️⃣ Clone Repository

git clone https://github.com/your-username/interview-intelligence-system.git

cd interview-intelligence-system

2️⃣ Install Requirements

pip install -r requirements.txt

3️⃣ Download Speech Model (Important)

This project uses a Vosk speech recognition model that is not included due to size.

Download from:
https://alphacephei.com/vosk/models

Model name: vosk-model-small-en-us-0.15

Extract it inside a folder named:
assets/

▶️ Run the App

streamlit run app.py

Then open the browser link shown in terminal.

💡 Future Improvements

• Facial emotion detection
• Advanced NLP answer evaluation
• Cloud deployment
• Resume vs Interview matching

👩‍💻 Author

Harini Nagireddy
B.Tech CSE (Data Science)

⭐ If you like this project, feel free to star the repository!
