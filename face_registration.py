import mysql.connector as mysql  
import os  
import cv2 
from db_connection import connect_to_db 


def register_face(name, roll_no):
    db = connect_to_db()
    cursor = db.cursor()

    # Save face data as images
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    face_data_dir = "faces"
    os.makedirs(face_data_dir, exist_ok=True)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y + h, x:x + w]
            count += 1
            filename = f"{face_data_dir}/{roll_no}_{count}.jpg"
            cv2.imwrite(filename, face_img)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Register Face", frame)

        if count >= 10:  # Save 10 images per student
            break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Insert student details into database
    try:
        cursor.execute("INSERT INTO Students (name, roll_no) VALUES (%s, %s)", (name, roll_no))
        db.commit()
    except mysql.connector.Error as e:
        print("Database error:", e)
    finally:
        cursor.close()
        db.close()
