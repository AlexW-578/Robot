import cv2
import numpy as np
import imutils
import time
from gpiozero import Motor
import remote
from PIL import Image

motor1 = Motor(25, 24)
motor2 = Motor(23, 22)

STOP = 0
FORWARD = 1
BACKWARD = 2
LEFT = 3
RIGHT = 4

now = 0
limit = 0
state = STOP
next = STOP


def colour():
    img = cv2.imread('colour.png')
    hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    lower_range = np.array([0, 100, 100])
    upper_range = np.array([5, 255, 255])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    # cv2.imshow('image', img)
    cv2.imshow('mask', mask)
    cv2.imwrite("mask.bmp", mask)
    im = Image.open('mask.bmp')
    pix = im.load()
    size = (im.size)
    for x in range(0, size[1]):
        for y in range(0, size[0]):
            if pix[x, y] == 255:
                print(pix[x, y])
    print(pix[432, 116])
    # pix[x,y] = value
    # im.save('alive_parrot.png')
    while (True):
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()


def action(key):
    global now, limit, next

    if key == "F":
        next = FORWARD;
        limit = now + 5
    elif key == "B":
        next = BACKWARD;
        limit = now + 5
    elif key == "L":
        next = LEFT;
        limit = now + 5
    elif key == "R":
        next = RIGHT;
        limit = now + 5
    elif key == "X":
        next = STOP


def update():
    global now, limit, state, next

    if now >= limit:
        next = STOP

    if next == state:
        return

    print("new state", next)

    if next == FORWARD:
        motor1.forward()
        motor2.forward()
    elif next == BACKWARD:
        motor1.backward()
        motor2.backward()
    elif next == LEFT:
        motor1.forward()
        motor2.stop()
    elif next == RIGHT:
        motor1.stop()
        motor2.forward()
    else:
        motor1.stop()
        motor2.stop()

    state = next


def mainloop():
    global now

    while True:

        while True:
            key = remote.getkey()
            if not key:
                break
            action(key)
        update()
        time.sleep(0.1)
        now += 1


mainloop()
