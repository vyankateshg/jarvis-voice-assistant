import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import Thread
from PIL import Image, ImageTk

# Directory to store user data
USER_DATA_PATH = r"C:\python project\jarvis meri jaan\face_picture"
os.makedirs(USER_DATA_PATH, exist_ok=True)

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        
        # GUI Components
        self.label = tk.Label(root, text="Face Recognition System", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.capture_button = tk.Button(root, text="Register New User", font=("Arial", 14), command=self.capture_user_images)
        self.capture_button.pack(pady=10)
        
        self.recognize_button = tk.Button(root, text="Recognize User", font=("Arial", 14), command=self.recognize_user)
        self.recognize_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit)
        self.quit_button.pack(pady=10)
        
        self.user_name_label = tk.Label(root, text="No user recognized yet", font=("Arial", 14))
        self.user_name_label.pack(pady=10)

        self.video_source = 0  # Default camera
        self.cap = cv2.VideoCapture(self.video_source)
        
        # Start video feed
        self.video_thread = Thread(target=self.video_loop)
        self.video_thread.daemon = True
        self.video_thread.start()

    def video_loop(self):
        """
        Loop to capture video from webcam and update GUI.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            # Convert frame to RGB (Tkinter uses RGB, OpenCV uses BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to PhotoImage format for Tkinter
            photo = self.convert_to_tkinter_image(frame_rgb)
            # Update the GUI image
            self.label.config(image=photo)
            self.label.image = photo

    def convert_to_tkinter_image(self, cv_image):
        """
        Convert OpenCV image (BGR) to Tkinter-compatible image (RGB).
        """
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert back to BGR
        return ImageTk.PhotoImage(image=Image.fromarray(img))

    def capture_user_images(self):
        """
        Capture images for a new user and store them in the specified folder.
        """
        user_name = simpledialog.askstring("Input", "Enter your name:")
        if user_name is None or user_name == "":
            messagebox.showerror("Error", "User name cannot be empty.")
            return
        
        user_folder = os.path.join(USER_DATA_PATH, user_name)
        os.makedirs(user_folder, exist_ok=True)
        
        # Start capturing images from webcam
        cap = cv2.VideoCapture(self.video_source)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        count = 0
        while count < 10:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                # Save face images
                face_resized = cv2.resize(face, (100, 100))
                cv2.imwrite(os.path.join(user_folder, f"{count}.jpg"), face_resized)
                count += 1
                break
            # Show the live feed
            cv2.imshow("Registering User", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", f"Images captured for user: {user_name}")

    def recognize_user(self):
        """
        Recognize a user from the webcam feed by comparing with stored faces.
        """
        cap = cv2.VideoCapture(self.video_source)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                # Draw rectangle around detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                captured_face = gray[y:y + h, x:x + w]
                captured_face_resized = cv2.resize(captured_face, (100, 100))
                
                # Compare with stored user faces
                recognized_user = None
                for user_name in os.listdir(USER_DATA_PATH):
                    user_folder = os.path.join(USER_DATA_PATH, user_name)
                    match_score = 0
                    total_images = 0
                    for img_name in os.listdir(user_folder):
                        stored_face = cv2.imread(os.path.join(user_folder, img_name), cv2.IMREAD_GRAYSCALE)
                        stored_face_resized = cv2.resize(stored_face, (100, 100))
                        score = cv2.compareHist(
                            cv2.calcHist([captured_face_resized], [0], None, [256], [0, 256]),
                            cv2.calcHist([stored_face_resized], [0], None, [256], [0, 256]),
                            cv2.HISTCMP_CORREL
                        )
                        match_score += score
                        total_images += 1
                    avg_score = match_score / total_images if total_images > 0 else 0
                    if avg_score > 0.8:
                        recognized_user = user_name
                        break
                
                if recognized_user:
                    self.user_name_label.config(text=f"Recognized User: {recognized_user}")
                    cv2.putText(frame, f"User: {recognized_user}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    break

            # Show live feed with recognition results
            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Create Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
