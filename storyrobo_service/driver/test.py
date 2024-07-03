# import Jetson.GPIO as GPIO
# import time

# button1_pin = 16
# button2_pin = 18
# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# try:
#     print("Press Ctrl+C to exit")
#     while True:
#         button_state = GPIO.input(button1_pin)
#         if button_state == GPIO.LOW:
#             print("Button 1 pressed")
#         else:
#             print("Button 1 not pressed")
#         # GPIO.wait_for_edge(button1_pin, GPIO.FALLING)
#         # print("Button 1 Trigger")
#         # GPIO.wait_for_edge(button2_pin, GPIO.FALLING)
#         # print("Button 2 Trigger")

#         time.sleep(0.15) 

# except KeyboardInterrupt:
#     print("Exiting program")

# finally:
#     GPIO.cleanup()  # Clean up GPIO on exit

import RPi.GPIO as GPIO
import time

but1_pin = 16
but2_pin = 18

# blink LED 2 quickly 5 times when button pressed
def but1(channel):
    print("btn1 pressed")

def but2(channel):
    print("btn2 pressed")

def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(but1_pin, GPIO.IN)  # button pin set as input
    GPIO.setup(but2_pin, GPIO.IN)  # button pin set as input

    # By default, the poll time is 0.2 seconds, too
    GPIO.add_event_detect(but1_pin, GPIO.FALLING, callback=but1, bouncetime=10, polltime=10)
    GPIO.add_event_detect(but2_pin, GPIO.FALLING, callback=but2, bouncetime=10, polltime=10)
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            time.sleep(2)
    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()