# Emotion Detector App 🎭

A Python-based application that performs real-time facial expression recognition. This project uses deep learning to detect emotions like happiness, sadness, anger, and more through a camera feed.

## 🚀 Features
* **Real-time Detection:** Process video frames instantly to identify emotions.
* **Cross-Platform:** Built using Kivy/Tkinter for compatibility.
* **Mobile Ready:** Includes configuration for Android deployment via Buildozer.

## 📲 How to Install (Android)
If you just want to use the app on your phone:
1. Go to the **[Releases](https://github.com/ranvirw18/emotion-detector-app/releases)** section of this repository.
2. Download the `.apk` file.
3. Transfer it to your Android device.
4. Enable "Install from Unknown Sources" in your phone settings and install the APK.

## 💻 How to Run (Development)
To run the code locally on your PC, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ranvirw18/emotion-detector-app.git](https://github.com/ranvirw18/emotion-detector-app.git)
   cd emotion-detector-app
Create a virtual environment:

Bash
python -m venv .venv
source .venv/scripts/activate  # On Windows use: .venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Run the app:

Bash
python main.py
🛠️ Tech Stack
Language: Python

GUI Framework: Tkinter / Kivy

Deployment: Buildozer (for Android APK)

Libraries: OpenCV, TensorFlow/Keras (for recognition logic)

📂 Project Structure
main.py: The entry point of the application.

facial_expression_recognizer.py: Contains the core emotion detection logic.

buildozer.spec: Configuration for building the Android package.

bin/: Contains the compiled executable/APK files.

Learning by building. Developed by Ranvir Wadhawan.