"""Android-ready Kivy UI for packaging this project as an APK.

The original Tkinter desktop implementation cannot run on Android. This file now
exposes a Kivy `EmotionDetectorApp` that matches `main.py` and Buildozer.
"""

from importlib import import_module

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

try:
    import cv2
    import numpy as np

    try:
        from fer import FER
    except ImportError:
        from fer.fer import FER
except Exception:
    cv2 = None
    np = None
    FER = None


class Permission:
    CAMERA = "android.permission.CAMERA"


def request_permissions(_permissions):
    return None


if platform == "android":
    try:
        _android_permissions = import_module("android.permissions")
        Permission = _android_permissions.Permission
        request_permissions = _android_permissions.request_permissions
    except Exception:
        pass

KV = """
<EmotionDetectorRoot>:
    orientation: "vertical"
    padding: "12dp"
    spacing: "10dp"

    canvas.before:
        Color:
            rgba: 0.07, 0.07, 0.08, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Emotion Detector"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: "42dp"
        color: 0.1, 0.9, 1, 1

    Camera:
        id: cam
        index: 0
        resolution: (640, 480)
        play: root.camera_running
        allow_stretch: True
        keep_ratio: True
        size_hint_y: 0.72

    Label:
        text: root.status_text
        font_size: "15sp"
        text_size: self.width, None
        halign: "center"
        valign: "middle"
        size_hint_y: None
        height: "52dp"
        color: 1, 1, 1, 1

    Label:
        text: root.emotion_text
        font_size: "18sp"
        bold: True
        size_hint_y: None
        height: "36dp"
        color: 1, 0.85, 0.2, 1

    BoxLayout:
        size_hint_y: None
        height: "52dp"
        spacing: "8dp"

        Button:
            text: "Start Camera"
            on_release: root.start_camera()

        Button:
            text: "Analyze Preview"
            on_release: root.analyze_preview()

        Button:
            text: "Stop"
            on_release: root.stop_camera()
"""


class EmotionDetectorRoot(BoxLayout):
    """Camera preview UI with live desktop emotion detection."""

    status_text = StringProperty("Tap Start Camera to begin.")
    emotion_text = StringProperty("Emotion: --")
    camera_running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.detector = None
        self._analysis_event = None
        self._setup_detector()

    def on_kv_post(self, _base_widget):
        self._request_camera_permission()

    def _setup_detector(self):
        if platform == "android":
            return

        if FER is None or cv2 is None or np is None:
            self.status_text = "Recognition dependencies are missing."
            return

        try:
            self.detector = FER(mtcnn=False)
        except Exception as exc:
            self.status_text = f"Detector load issue: {exc}"

    def _request_camera_permission(self):
        if platform != "android":
            return

        try:
            request_permissions([Permission.CAMERA])
            self.status_text = "Camera permission requested."
        except Exception as exc:
            self.status_text = f"Permission notice: {exc}"

    def _get_current_frame(self):
        texture = self.ids.cam.texture
        if texture is None or np is None or cv2 is None:
            return None

        width, height = texture.size
        frame = np.frombuffer(texture.pixels, dtype=np.uint8)
        expected_size = width * height * 4
        if frame.size != expected_size:
            return None

        frame = frame.reshape(height, width, 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        frame = cv2.flip(frame, 0)
        return frame

    def _analyze_frame(self, *_args):
        if not self.camera_running:
            return

        if self.detector is None:
            if platform == "android":
                self.status_text = "Camera works on Android; add a TFLite model for mobile detection."
                self.emotion_text = "Emotion: mobile model not added yet"
            else:
                self.status_text = "Detector is unavailable on this device."
            return

        frame = self._get_current_frame()
        if frame is None:
            self.status_text = "Waiting for camera frame..."
            return

        try:
            results = self.detector.detect_emotions(frame)
            if not results:
                self.status_text = "No face detected. Face the camera clearly."
                self.emotion_text = "Emotion: no face detected"
                return

            emotions = results[0].get("emotions", {})
            if not emotions:
                self.status_text = "Face found, but emotion scores are unavailable."
                self.emotion_text = "Emotion: unavailable"
                return

            dominant = max(emotions, key=emotions.get)
            confidence = emotions[dominant] * 100
            self.status_text = "Face recognized successfully."
            self.emotion_text = f"Emotion: {dominant.capitalize()} ({confidence:.1f}%)"
        except Exception as exc:
            self.status_text = f"Detection error: {exc}"

    def start_camera(self):
        self.camera_running = True
        self.ids.cam.play = True

        if self.detector is not None:
            self.status_text = "Camera is live. Scanning for emotion..."
            self.emotion_text = "Emotion: scanning..."
            if self._analysis_event is None:
                self._analysis_event = Clock.schedule_interval(self._analyze_frame, 1.0)
        else:
            self.status_text = "Camera is live."
            self.emotion_text = "Emotion: unavailable"

    def stop_camera(self):
        self.camera_running = False
        self.ids.cam.play = False
        if self._analysis_event is not None:
            self._analysis_event.cancel()
            self._analysis_event = None
        self.status_text = "Camera stopped."
        self.emotion_text = "Emotion: --"

    def analyze_preview(self):
        if not self.camera_running:
            self.status_text = "Start the camera first."
            return

        self._analyze_frame()


class EmotionDetectorApp(App):
    def build(self):
        self.title = "Emotion Detector"
        Builder.load_string(KV)
        return EmotionDetectorRoot()

    def on_stop(self):
        if self.root:
            self.root.stop_camera()


if __name__ == "__main__":
    EmotionDetectorApp().run()