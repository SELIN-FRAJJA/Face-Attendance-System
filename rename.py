import face_recognition
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Paths to known and unknown face images
known_faces_dir = r"E:\Face-Recognition-Attendance-Projects\Training_images2"
test_faces_dir = r"E:\Face-Recognition-Attendance-Projects\test"

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir(known_faces_dir):
    image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(os.path.splitext(filename)[0])  # Extract name from filename

# Lists to store actual vs. predicted labels for metrics calculation
actual_labels = []
predicted_labels = []

# Process test faces
for filename in os.listdir(test_faces_dir):
    image = face_recognition.load_image_file(f"{test_faces_dir}/{filename}")
    actual_name = os.path.splitext(filename)[0]  # Known label from file name
    actual_labels.append(actual_name)

    # Detect and encode faces in test image
    test_face_encodings = face_recognition.face_encodings(image)
    
    if test_face_encodings:  # If face is found in the test image
        test_encoding = test_face_encodings[0]
        
        # Compare with known faces
        results = face_recognition.compare_faces(known_face_encodings, test_encoding,  tolerance=0.5)
        distances = face_recognition.face_distance(known_face_encodings, test_encoding)
        
        # Choose the best match (if a match is found)
        best_match_index = np.argmin(distances) if any(results) else None
        
        if best_match_index is not None and results[best_match_index]:
            predicted_name = known_face_names[best_match_index]
        else:
            predicted_name = "Unknown"  # Mark as unknown if no match
    else:
        predicted_name = "Unknown"  # No face found

    predicted_labels.append(predicted_name)

# Calculate accuracy metrics
accuracy = accuracy_score(actual_labels, predicted_labels)
precision = precision_score(actual_labels, predicted_labels, average='weighted', zero_division=1)
recall = recall_score(actual_labels, predicted_labels, average='weighted', zero_division=1)
conf_matrix = confusion_matrix(actual_labels, predicted_labels, labels=known_face_names + ["Unknown"])

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("Confusion Matrix:\n", conf_matrix)
