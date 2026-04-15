import cv2
import face_recognition
import numpy as np

class FaceRecognitionManager:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def capture_faces(self, image_path):
        # Load an image and get face locations and encodings
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        return face_locations, face_encodings

    def add_face(self, image_path, name):
        # Capture faces and add their encoding and name to the lists
        face_locations, face_encodings = self.capture_faces(image_path)
        if face_encodings:
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_names.append(name)

    def recognize_faces(self, image_path):
        # Recognize faces in an image
        image = face_recognition.load_image_file(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            face_names.append(name)

        return face_locations, face_names

    def draw_face_boxes(self, image_path):
        # Draw boxes around recognized faces
        image = cv2.imread(image_path)
        face_locations, face_names = self.recognize_faces(image_path)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return image

    def save_image(self, image, output_path):
        cv2.imwrite(output_path, image)
