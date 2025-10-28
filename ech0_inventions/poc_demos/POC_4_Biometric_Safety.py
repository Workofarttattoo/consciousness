#!/usr/bin/env python3
"""
POC #4: Biometric Ride Safety Pre-Check
FREE - Uses webcam + OpenCV
"""
import cv2
import time

print("🏥 Biometric Safety Pre-Check - POC Demo")
print("Simulating heart rate detection from webcam")
print()

# Simulate biometric monitoring
cap = cv2.VideoCapture(0)

# Simple face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

start_time = time.time()
heart_rate_sim = 70  # Simulated

while time.time() - start_time < 30:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect face
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Simulate heart rate variation
    heart_rate_sim = 70 + int(5 * (time.time() % 10) / 10)

    # Draw overlay
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"HR: {heart_rate_sim} bpm", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if heart_rate_sim > 100:
            cv2.putText(frame, "ALERT: Elevated HR", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Biometric Safety Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ Demo complete!")
print("Next: Add real pulse detection via webcam color changes")
