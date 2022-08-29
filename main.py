import os
import cv2
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication,QWidget,QFileDialog
from PyQt6.QtWidgets import QVBoxLayout, QLabel,QPushButton
from PyQt6.QtCore import Qt

def pics_dialog():
    pics, _ = QFileDialog.getOpenFileNames(window, 'Select Files')
    choose_label.setText('\n'.join(pics))

def target_dialog():
    target = str(QFileDialog.getExistingDirectory(window, "Select Directory"))
    destination_label.setText(target)

def crop_faces():
    pics = choose_label.text().split("\n")
    target = destination_label.text()
    for image_path in pics:
        img_name = os.path.basename(image_path)
        image = cv2.imread(image_path,1)
        faces = face_cascade.detectMultiScale(image,1.1,4)
        cnt=0
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 4)
            roi = image[y:y + h, x:x + w]
            cv2.imwrite(f'{target}/{img_name}-face_{cnt}.jpeg', roi)
            cnt += 1
    crop_label.setText("Faces Cropped!")

face_cascade = cv2.CascadeClassifier('resources/faces.xml')

app = QApplication([])
window = QWidget()
window.setWindowTitle("Face Detect & Crop")
layout = QVBoxLayout()

description = QLabel("""Choose pictures and let the program automatically crop
 out the faces into destination folder""")
layout.addWidget(description,alignment=Qt.AlignmentFlag.AlignCenter)

choose_btn = QPushButton("Choose Pics")
layout.addWidget(choose_btn)
choose_label= QLabel("")
layout.addWidget(choose_btn)
layout.addWidget(choose_label)
choose_btn.clicked.connect(pics_dialog)

destination_btn = QPushButton("Choose destination folder")
destination_label = QLabel("")
layout.addWidget(destination_btn)
layout.addWidget(destination_label)
destination_btn.clicked.connect(target_dialog)

crop_btn = QPushButton("Cut out faces!")
layout.addWidget(crop_btn)
crop_label = QLabel("")
layout.addWidget(crop_label,alignment=Qt.AlignmentFlag.AlignCenter)
crop_btn.clicked.connect(crop_faces)

window.setLayout(layout)
window.show()
app.exec()