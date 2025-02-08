import cv2
import numpy as np
import face_recognition
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Path to the training and test images
train_path = r'E:\Face-Recognition-Attendance-Projects\Training_images2'
test_path = r'E:\Face-Recognition-Attendance-Projects\Test_images'

# Load training images
train_images = []
classNames = []
train_list = os.listdir(train_path)
print("Training Class Names:", train_list)

for cl in train_list:
    curImg = cv2.imread(f'{train_path}/{cl}')
    train_images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Load test images and labels
test_images = []
test_labels = []
test_list = os.listdir(test_path)

for img_name in test_list:
    testImg = cv2.imread(f'{test_path}/{img_name}')
    test_images.append(testImg)
    test_labels.append(os.path.splitext(img_name)[0])

print("Test Labels:", test_labels)

# Encode training images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            encodeList.append(encode[0])
    return encodeList

encodeListKnown = findEncodings(train_images)
print('Encoding Complete')

# Lists to store actual and predicted labels for the test images
actual_labels = []
predicted_labels = []

# Process each test image
for img, actual_name in zip(test_images, test_labels):
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Default prediction for this image is "Unknown"
    predicted_name = "Unknown"

    if encodesCurFrame:  # Only process if encodings were found
        for encodeFace in encodesCurFrame:
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                predicted_name = classNames[matchIndex].upper()

    # Store actual and predicted labels
    actual_labels.append(actual_name.upper())
    predicted_labels.append(predicted_name)

# Calculate accuracy, precision, recall, and confusion matrix
accuracy = accuracy_score(actual_labels, predicted_labels)
precision = precision_score(actual_labels, predicted_labels, average='weighted', zero_division=0)  # Change to zero_division=0
recall = recall_score(actual_labels, predicted_labels, average='weighted', zero_division=0)  # Change to zero_division=0
conf_matrix = confusion_matrix(actual_labels, predicted_labels, labels=classNames + ["Unknown"])

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print("Confusion Matrix:")
print(conf_matrix)
