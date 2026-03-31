[app]
title = Emotion Detector
package.name = emotiondetector
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = CAMERA
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
