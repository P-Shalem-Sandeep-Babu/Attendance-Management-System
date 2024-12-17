from datetime import datetime
import os
import cv2
import mysql.connector as mysql
from face_registration import face_recognition 
from db_connection import connect_to_db


def mark_attendance():
    db = connect_to_db()
    cursor = db.cursor()

    known_faces = []
    roll_numbers = []

    # Load registered faces
    for student in os.listdir("faces"):
        roll_no = student.split("_")[0]
        image = face_recognition.load_image_file(f"faces/{student}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        roll_numbers.append(roll_no)

    # Start camera for attendance
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, encoding)
            if True in matches:
                match_index = matches.index(True)
                roll_no = roll_numbers[match_index]

                now = datetime.now()
                date = now.date()
                time = now.time()

                # Insert attendance record
                try:
                    cursor.execute(
                        "INSERT INTO Attendance (roll_no, date, time) VALUES (%s, %s, %s)",
                        (roll_no, date, time)
                    )
                    db.commit()
                except mysql.connector.Error as e:
                    print("Attendance marking error:", e)

                # Display the name on the screen
                y1, x2, y2, x1 = location
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, roll_no, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Mark Attendance", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    db.close()
