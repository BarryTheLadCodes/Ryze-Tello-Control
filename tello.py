import time
from djitellopy import Tello
import cv2
import threading
import keyboard
import os

S = 60
FPS = 60
tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()

left_right_velocity = 0
for_back_velocity = 0
up_down_velocity = 0
yaw_velocity = 0

speed = 10
tello.connect()
tello.set_speed(speed)
tello.takeoff()

def move():
    while True:
        if keyboard.is_pressed('up arrow'):
            for_back_velocity = S
        elif keyboard.is_pressed('right arrow'):
            left_right_velocity = S
        elif keyboard.is_pressed('down arrow'):
            for_back_velocity = -S
        elif keyboard.is_pressed('left arrow'):
            left_right_velocity = -S
        elif keyboard.is_pressed('w'):
            up_down_velocity = S
        elif keyboard.is_pressed('d'):
            yaw_velocity = S
        elif keyboard.is_pressed('s'):
            up_down_velocity = -S
        elif keyboard.is_pressed('a'):
            yaw_velocity = -S
        elif keyboard.is_pressed('l'):
            tello.land()
        else:
            for_back_velocity = 0
            left_right_velocity = 0
            up_down_velocity = 0
            yaw_velocity = 0
        tello.send_rc_control(left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity)
        os.system('cls')

thread_move = threading.Thread(target=move)
thread_move.start()

frame_read = tello.get_frame_read()
while True:
    img = frame_read.frame
    cv2.putText(img, f'Battery: {tello.get_battery()}', (10, 30 - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.resize(img, (1000,1000))
    cv2.imshow("drone", img)

    time.sleep(1/FPS)
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        break
tello.land()
cv2.destroyAllWindows()