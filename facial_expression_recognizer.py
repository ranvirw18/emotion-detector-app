# """Android-ready Kivy UI for packaging this project as an APK.

# The original Tkinter desktop implementation cannot run on Android. This file now
# exposes a Kivy `EmotionDetectorApp` that matches `main.py` and Buildozer.
# """

# from importlib import import_module
# import os

# from kivy.app import App
# from kivy.clock import Clock
# from kivy.lang import Builder
# from kivy.properties import BooleanProperty, StringProperty
# from kivy.uix.boxlayout import BoxLayout
# from kivy.utils import platform

# try:
#     import cv2
#     import numpy as np

#     try:
#         from fer import FER
#     except ImportError:
#         from fer.fer import FER
# except Exception:
#     cv2 = None
#     np = None
#     FER = None

# try:
#     import tensorflow as tf
# except Exception:
#     tf = None


# class TFLiteEmotionDetector:
#     """Lightweight TFLite-based emotion detector for mobile devices."""
    
#     EMOTIONS = ["angry", "disgusted", "fearful", "happy", "neutral", "sad", "surprised"]
#     FACE_DETECTOR_PATH = None  # Will be set dynamically
#     EMOTION_MODEL_PATH = None  # Will be set dynamically
    
#     def __init__(self):
#         self.face_detector_interpreter = None
#         self.emotion_interpreter = None
#         self.face_detector_input_details = None
#         self.face_detector_output_details = None
#         self.emotion_input_details = None
#         self.emotion_output_details = None
#         self._load_models()
    
#     def _load_models(self):
#         """Load TFLite models for face detection and emotion classification."""
#         try:
#             if tf is None:
#                 raise ImportError("TensorFlow not available")
            
#             # Try to load pre-converted models or use MediaPipe face detection
#             # For now, we'll use a simplified approach with OpenCV face cascade
#             self.cascade_classifier = cv2.CascadeClassifier(
#                 cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
#             )
            
#             # Load emotion model if available, otherwise use a simple classifier
#             model_path = self._find_emotion_model()
#             if model_path and os.path.exists(model_path):
#                 self.emotion_interpreter = tf.lite.Interpreter(model_path)
#                 self.emotion_interpreter.allocate_tensors()
#                 self.emotion_input_details = self.emotion_interpreter.get_input_details()
#                 self.emotion_output_details = self.emotion_interpreter.get_output_details()
#             else:
#                 # Initialize with a simple pre-trained model if available
#                 self._init_default_emotion_model()
#         except Exception as e:
#             print(f"Warning: Could not load TFLite models: {e}")
#             self.cascade_classifier = None
    
#     def _find_emotion_model(self):
#         """Look for emotion detection model in common locations."""
#         possible_paths = [
#             "emotion_model.tflite",
#             "models/emotion_model.tflite",
#             os.path.join(os.path.dirname(__file__), "emotion_model.tflite"),
#         ]
#         for path in possible_paths:
#             if os.path.exists(path):
#                 return path
#         return None
    
#     def _init_default_emotion_model(self):
#         """Initialize a default emotion model if TFLite model not found."""
#         # This uses a placeholder approach - in production, include a trained model
#         self.use_simple_classifier = True
    
#     def detect_emotions(self, frame):
#         """Detect emotions in the given frame.
        
#         Returns:
#             list: List of detected faces with emotions, similar to FER format
#         """
#         if frame is None or cv2 is None:
#             return []
        
#         try:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = self.cascade_classifier.detectMultiScale(
#                 gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
#             )
            
#             if len(faces) == 0:
#                 return []
            
#             results = []
#             for (x, y, w, h) in faces:
#                 # Extract face region
#                 face_roi = frame[y:y+h, x:x+w]
#                 face_roi = cv2.resize(face_roi, (48, 48))
#                 face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
                
#                 # Predict emotion
#                 emotion = self._predict_emotion(face_roi)
                
#                 results.append({
#                     "box": {"x": x, "y": y, "w": w, "h": h},
#                     "emotions": emotion,
#                 })
            
#             return results
#         except Exception as e:
#             print(f"Error detecting emotions: {e}")
#             return []
    
#     def _predict_emotion(self, face_roi):
#         """Predict emotion for a given face ROI."""
#         if self.emotion_interpreter is not None:
#             try:
#                 # Prepare input
#                 input_data = np.expand_dims(face_roi, axis=(0, 3)).astype(np.float32) / 255.0
                
#                 self.emotion_interpreter.set_tensor(
#                     self.emotion_input_details[0]["index"], input_data
#                 )
#                 self.emotion_interpreter.invoke()
                
#                 output_data = self.emotion_interpreter.get_tensor(
#                     self.emotion_output_details[0]["index"]
#                 )[0]
                
#                 emotion_dict = {
#                     emotion: float(score) 
#                     for emotion, score in zip(self.EMOTIONS, output_data)
#                 }
#                 return emotion_dict
#             except Exception as e:
#                 print(f"Error in emotion inference: {e}")
        
#         # Simple fallback: return random-like confidence based on face properties
#         return {emotion: 1.0 / len(self.EMOTIONS) for emotion in self.EMOTIONS}


# class Permission:
#     CAMERA = "android.permission.CAMERA"


# def request_permissions(_permissions):
#     return None


# if platform == "android":
#     try:
#         _android_permissions = import_module("android.permissions")
#         Permission = _android_permissions.Permission
#         request_permissions = _android_permissions.request_permissions
#     except Exception:
#         pass

# KV = """
# <EmotionDetectorRoot>:
#     orientation: "vertical"
#     padding: "12dp"
#     spacing: "10dp"

#     canvas.before:
#         Color:
#             rgba: 0.07, 0.07, 0.08, 1
#         Rectangle:
#             pos: self.pos
#             size: self.size

#     Label:
#         text: "Emotion Detector"
#         font_size: "24sp"
#         bold: True
#         size_hint_y: None
#         height: "42dp"
#         color: 0.1, 0.9, 1, 1

#     Camera:
#         id: cam
#         index: 0
#         resolution: (640, 480)
#         play: root.camera_running
#         allow_stretch: True
#         keep_ratio: True
#         size_hint_y: 0.72

#     Label:
#         text: root.status_text
#         font_size: "15sp"
#         text_size: self.width, None
#         halign: "center"
#         valign: "middle"
#         size_hint_y: None
#         height: "52dp"
#         color: 1, 1, 1, 1

#     Label:
#         text: root.emotion_text
#         font_size: "18sp"
#         bold: True
#         size_hint_y: None
#         height: "36dp"
#         color: 1, 0.85, 0.2, 1

#     BoxLayout:
#         size_hint_y: None
#         height: "52dp"
#         spacing: "8dp"

#         Button:
#             text: "Start Camera"
#             on_release: root.start_camera()

#         Button:
#             text: "Analyze Preview"
#             on_release: root.analyze_preview()

#         Button:
#             text: "Stop"
#             on_release: root.stop_camera()
# """


# class EmotionDetectorRoot(BoxLayout):
#     """Camera preview UI with live desktop emotion detection."""

#     status_text = StringProperty("Tap Start Camera to begin.")
#     emotion_text = StringProperty("Emotion: --")
#     camera_running = BooleanProperty(False)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.detector = None
#         self.detector_type = None
#         self._analysis_event = None
#         self._setup_detector()

#     def on_kv_post(self, _base_widget):
#         self._request_camera_permission()

#     def _setup_detector(self):
#         if FER is None or cv2 is None or np is None:
#             self.status_text = "Recognition dependencies are missing."
#             return

#         try:
#             if platform == "android":
#                 # Use TFLite for mobile
#                 self.detector = TFLiteEmotionDetector()
#                 self.detector_type = "tflite"
#             else:
#                 # Use FER for desktop
#                 self.detector = FER(mtcnn=False)
#                 self.detector_type = "fer"
#         except Exception as exc:
#             self.status_text = f"Detector load issue: {exc}"

#     def _request_camera_permission(self):
#         if platform != "android":
#             return

#         try:
#             request_permissions([Permission.CAMERA])
#             self.status_text = "Camera permission requested."
#         except Exception as exc:
#             self.status_text = f"Permission notice: {exc}"

#     def _get_current_frame(self):
#         texture = self.ids.cam.texture
#         if texture is None or np is None or cv2 is None:
#             return None

#         width, height = texture.size
#         frame = np.frombuffer(texture.pixels, dtype=np.uint8)
#         expected_size = width * height * 4
#         if frame.size != expected_size:
#             return None

#         frame = frame.reshape(height, width, 4)
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
#         frame = cv2.flip(frame, 0)
#         return frame

#     def _analyze_frame(self, *_args):
#         if not self.camera_running:
#             return

#         if self.detector is None:
#             self.status_text = "Detector is unavailable. Please restart the app."
#             self.emotion_text = "Emotion: unavailable"
#             return

#         frame = self._get_current_frame()
#         if frame is None:
#             self.status_text = "Waiting for camera frame..."
#             return

#         try:
#             results = self.detector.detect_emotions(frame)
#             if not results:
#                 self.status_text = "No face detected. Face the camera clearly."
#                 self.emotion_text = "Emotion: no face detected"
#                 return

#             emotions = results[0].get("emotions", {})
#             if not emotions:
#                 self.status_text = "Face found, but emotion scores are unavailable."
#                 self.emotion_text = "Emotion: unavailable"
#                 return

#             dominant = max(emotions, key=emotions.get)
#             confidence = emotions[dominant] * 100
#             detector_info = f"({self.detector_type})" if self.detector_type else ""
#             self.status_text = f"Face recognized successfully. {detector_info}"
#             self.emotion_text = f"Emotion: {dominant.capitalize()} ({confidence:.1f}%)"
#         except Exception as exc:
#             self.status_text = f"Detection error: {exc}"

#     def start_camera(self):
#         self.camera_running = True
#         self.ids.cam.play = True

#         if self.detector is not None:
#             self.status_text = "Camera is live. Scanning for emotion..."
#             self.emotion_text = "Emotion: scanning..."
#             if self._analysis_event is None:
#                 self._analysis_event = Clock.schedule_interval(self._analyze_frame, 1.0)
#         else:
#             self.status_text = "Camera is live."
#             self.emotion_text = "Emotion: unavailable"

#     def stop_camera(self):
#         self.camera_running = False
#         self.ids.cam.play = False
#         if self._analysis_event is not None:
#             self._analysis_event.cancel()
#             self._analysis_event = None
#         self.status_text = "Camera stopped."
#         self.emotion_text = "Emotion: --"

#     def analyze_preview(self):
#         if not self.camera_running:
#             self.status_text = "Start the camera first."
#             return

#         self._analyze_frame()


# class EmotionDetectorApp(App):
#     def build(self):
#         self.title = "Emotion Detector"
#         Builder.load_string(KV)
#         return EmotionDetectorRoot()

#     def on_stop(self):
#         if self.root:
#             self.root.stop_camera()


# if __name__ == "__main__":
#     EmotionDetectorApp().run()



#tflite


# from importlib import import_module
# import os

# from kivy.app import App
# from kivy.clock import Clock
# from kivy.lang import Builder
# from kivy.properties import BooleanProperty, StringProperty
# from kivy.uix.boxlayout import BoxLayout
# from kivy.utils import platform

# import cv2
# import numpy as np

# try:
#     import tensorflow as tf
# except Exception:
#     tf = None


# # =========================
# # 🔥 REAL EMOTION DETECTOR
# # =========================
# class TFLiteEmotionDetector:
#     EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

#     def __init__(self):
#         if tf is None:
#             raise Exception("TensorFlow not installed")

#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#         )

#         model_path = "emotion_model.tflite"

#         if not os.path.exists(model_path):
#             raise Exception("❌ emotion_model.tflite NOT FOUND")

#         self.interpreter = tf.lite.Interpreter(model_path=model_path)
#         self.interpreter.allocate_tensors()

#         self.input_details = self.interpreter.get_input_details()
#         self.output_details = self.interpreter.get_output_details()

#     def detect_emotions(self, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         faces = self.face_cascade.detectMultiScale(
#             gray, scaleFactor=1.3, minNeighbors=5
#         )

#         results = []

#         for (x, y, w, h) in faces:
#             face = gray[y:y+h, x:x+w]

#             face = cv2.resize(face, (48, 48))
#             face = face / 255.0
#             face = np.reshape(face, (1, 48, 48, 1)).astype("float32")

#             self.interpreter.set_tensor(
#                 self.input_details[0]["index"], face
#             )
#             self.interpreter.invoke()

#             preds = self.interpreter.get_tensor(
#                 self.output_details[0]["index"]
#             )[0]

#             emotion_dict = {
#                 emotion: float(score)
#                 for emotion, score in zip(self.EMOTIONS, preds)
#             }

#             results.append({
#                 "box": {"x": x, "y": y, "w": w, "h": h},
#                 "emotions": emotion_dict
#             })

#         return results


# # =========================
# # PERMISSIONS
# # =========================
# class Permission:
#     CAMERA = "android.permission.CAMERA"


# def request_permissions(_permissions):
#     return None


# if platform == "android":
#     try:
#         _android_permissions = import_module("android.permissions")
#         Permission = _android_permissions.Permission
#         request_permissions = _android_permissions.request_permissions
#     except Exception:
#         pass


# # =========================
# # UI
# # =========================
# KV = """
# <EmotionDetectorRoot>:
#     orientation: "vertical"
#     padding: "12dp"
#     spacing: "10dp"

#     canvas.before:
#         Color:
#             rgba: 0.07, 0.07, 0.08, 1
#         Rectangle:
#             pos: self.pos
#             size: self.size

#     Label:
#         text: "Emotion Detector"
#         font_size: "24sp"
#         bold: True
#         size_hint_y: None
#         height: "42dp"
#         color: 0.1, 0.9, 1, 1

#     Camera:
#         id: cam
#         index: 0
#         resolution: (1280, 720)
#         play: root.camera_running
#         allow_stretch: True
#         keep_ratio: True
#         size_hint_y: 0.72

#     Label:
#         text: root.status_text
#         font_size: "15sp"
#         size_hint_y: None
#         height: "50dp"

#     Label:
#         text: root.emotion_text
#         font_size: "20sp"
#         bold: True
#         size_hint_y: None
#         height: "40dp"

#     BoxLayout:
#         size_hint_y: None
#         height: "50dp"
#         spacing: "8dp"

#         Button:
#             text: "Start"
#             on_release: root.start_camera()

#         Button:
#             text: "Stop"
#             on_release: root.stop_camera()
# """


# # =========================
# # ROOT LOGIC
# # =========================
# class EmotionDetectorRoot(BoxLayout):
#     status_text = StringProperty("Press Start")
#     emotion_text = StringProperty("Emotion: --")
#     camera_running = BooleanProperty(False)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.detector = None
#         self._event = None

#         try:
#             self.detector = TFLiteEmotionDetector()
#             self.status_text = "Model loaded ✅"
#         except Exception as e:
#             self.status_text = str(e)

#     def _get_frame(self):
#         texture = self.ids.cam.texture
#         if texture is None:
#             return None

#         w, h = texture.size
#         frame = np.frombuffer(texture.pixels, dtype=np.uint8)

#         if frame.size != w * h * 4:
#             return None

#         frame = frame.reshape(h, w, 4)
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
#         frame = cv2.flip(frame, 0)

#         return frame

#     def _analyze(self, dt):
#         if not self.camera_running or self.detector is None:
#             return

#         frame = self._get_frame()
#         if frame is None:
#             self.status_text = "Waiting camera..."
#             return

#         results = self.detector.detect_emotions(frame)

#         if not results:
#             self.emotion_text = "No face"
#             return

#         emotions = results[0]["emotions"]
#         dominant = max(emotions, key=emotions.get)
#         confidence = emotions[dominant]

#         if confidence < 0.4:
#             self.emotion_text = "Uncertain"
#         else:
#             self.emotion_text = f"{dominant} ({confidence*100:.1f}%)"

#         self.status_text = "Detecting..."

#     def start_camera(self):
#         self.camera_running = True
#         self.ids.cam.play = True

#         if self._event is None:
#             self._event = Clock.schedule_interval(self._analyze, 1)

#     def stop_camera(self):
#         self.camera_running = False
#         self.ids.cam.play = False

#         if self._event:
#             self._event.cancel()
#             self._event = None

#         self.status_text = "Stopped"
#         self.emotion_text = "Emotion: --"


# # =========================
# # APP
# # =========================
# class EmotionDetectorApp(App):
#     def build(self):
#         Builder.load_string(KV)
#         return EmotionDetectorRoot()


# if __name__ == "__main__":
#     EmotionDetectorApp().run()


####tkinter workable
import cv2
from fer.fer import FER
import tkinter as tk
from PIL import Image, ImageTk

# Initialize detector
detector = FER(mtcnn=True)

# Start webcam
cap = cv2.VideoCapture(0)

# Tkinter window
root = tk.Tk()
root.title("Emotion Detector")

label = tk.Label(root)
label.pack()

emotion_label = tk.Label(root, text="Emotion: --", font=("Arial", 16))
emotion_label.pack()


def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Detect emotions
    results = detector.detect_emotions(frame)

    if results:
        emotions = results[0]["emotions"]
        dominant = max(emotions, key=emotions.get)
        confidence = emotions[dominant]

        if confidence > 0.4:
            emotion_label.config(
                text=f"Emotion: {dominant} ({confidence*100:.1f}%)"
            )
        else:
            emotion_label.config(text="Emotion: Uncertain")

        # Draw box
        (x, y, w, h) = (
            results[0]["box"][0],
            results[0]["box"][1],
            results[0]["box"][2],
            results[0]["box"][3],
        )

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    else:
        emotion_label.config(text="No face detected")

    # Convert to Tkinter format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    label.imgtk = imgtk
    label.configure(image=imgtk)

    label.after(10, update_frame)


update_frame()

def on_close():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()