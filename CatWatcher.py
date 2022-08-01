#!/usr/bin/python3
# real-time object detection program from a live camera feed
# copied code from <Hello AI World NVDIA JETSON>

import jetson.inference
import jetson.utils
from datetime import datetime, date, timedelta
import time
import smtplib, ssl
import csv
from pathlib import Path
import logging
import os
import uuid


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def email_alert(time, duration):
    """
    Send notifications to the user whenever the cat enters or leaves the camera sight.
    Currently it's not secure as I have hardcoded password in my code and I have to lower gmail security level to make this work.
    An optimation is needed or notification should be sent using a different method.
    """
    port = 465
    context = ssl.create_default_context()
    sender_email = "emma.lijing0723@gmail.com"
    receiver_email = "regent.rosinski@gmail.com"

    if duration == 0:
        message = f"""\
		Subject: Cat-LitterBox Alert


		Hey you! It's {time} now.
		Your cat is in the litterbox!"""
    else:
        message = f"""\
		Subject: Cat-LitterBox Alert


		Hey again!
		Your cat left the litterbox at {time}.
		He used the toilet for {duration}."""

    # create a secure connection with Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(sender_email, "Jingdong1106!")
            server.sendmail(sender_email, receiver_email, message)
        except smtplib.SMTPAuthenticationError:
            logger.error("Email not working due to authentification error.")
        except OSError:
            logger.error("Email not working due to OS error.")


def _record_data_in_csv(
    username,
    entry_timestamp_epoch,
    depart_timestamp_epoch,
    toilet_duration,
):
    """
    Record time data to csv file (the only one)
    :param username: the username entered by the user
    :param entry_timestamp_readable: the time when the cat enters the litterbox
    :param depart_timestamp_readable: the time when the cat departs the litterbox
    :param toilet_duration: the duration of the cat at the litterbox
    """
    # date_of_the_day = date.today().strftime("%m-%d-%Y")
    date_of_the_day = date.today()
    entry_timestamp_readable = datetime.fromtimestamp(entry_timestamp_epoch).strftime(
        "%Y%m%d_%H:%M:%S"
    )
    # Name of the csv file is the combination of the username and the
    path_to_csvfile = (
        f"/home/emma_dev22/CatWatcher/output/{username}+{entry_timestamp_readable}"
    )

    # Open or create the csv file
    with open(path_to_csvfile, "a", newline="") as f:
        theWriter = csv.writer(f)
        # The file is empty
        if os.stat(path_to_csvfile).st_size == 0:
            theWriter.writerow(["date", "entry", "depart", "duration"])
        theWriter.writerow(
            [
                date_of_the_day,
                entry_timestamp_epoch,
                depart_timestamp_epoch,
                toilet_duration,
            ]
        )


def cat_watcher(username):
    """
    A camera is constantly monitoring at the litterbox to see if the cat shows up.
    Notifications will be sent to the user whenever the cat shows up or leaves the litterbox.
    Data of the times when cat shows up and leaves the litterbox is recorded in a csv file.
    """
    cat_absent_duration_second = 0
    entry_timestamp_epoch = None

    # while display.IsStreaming():
    while True:
        cat_is_here = False
        # Capture the next video frame from the camera
        # Camera.Capture() will wait until the next frame has been sent from the camera and loaded into GPU memory
        # The returned image will be a jetson.utils.cudaImage object that contains atributes like width, height, and pixel format
        img = camera.Capture()
        # Process the image with net.Detect() function. It returns a list of detections(detecting Objects)
        detections = net.Detect(img)
        # visualize the results with OpenGL (optional)
        display.Render(img)
        display.SetStatus(f"Object Detection | Network {net.GetNetworkFPS()} FPS")

        for detection in detections:
            if net.GetClassDesc(detection.ClassID) == "cat":
                logger.info("Detected a cat!")
                cat_is_here = True

        if cat_is_here is False:
            if entry_timestamp_epoch != None:
                # If cat is not present for more than 15 seconds, the program determines that the cat has left the litter box
                if cat_absent_duration_second < 15:
                    cat_absent_duration_second += 1
                    logger.info(
                        f"Emma, your cat has not been seen in the litterbox for {cat_absent_duration_second} seconds."
                    )
                else:
                    # Record the time when the cat left the litterbox
                    depart_timestamp_epoch = time.time() - 15
                    # Record the amount of time that cat used the litterbox
                    # toilet_duration_readable = time.strftime(
                    #    "%H:%M:%S",
                    #    time.gmtime(depart_timestamp_epoch - entry_timestamp_epoch),
                    # )
                    toilet_duration = depart_timestamp_epoch - entry_timestamp_epoch
                    # Send email alert of cat leaving the litterbox
                    # email_alert(depart_timestamp_readable, toilet_duration)
                    _record_data_in_csv(
                        username,
                        entry_timestamp_epoch,
                        depart_timestamp_epoch,
                        toilet_duration,
                    )
                    # Recall the function itself
                    cat_watcher(username)
        else:
            # Record the time when cat first shows up
            if entry_timestamp_epoch == None:
                entry_timestamp_epoch = time.time()
                # Send email alert of cat showing up at litterbox
                # email_alert(entry_timestamp_readable, 0)
            else:
                if -1 < cat_absent_duration_second < 16:
                    # Set cat_absent_duration_second to 0 if cat shows up again within 10 secs.
                    cat_absent_duration_second = 0
                else:
                    logger.error(
                        f"The cat's absence time has an invalid value of {cat_absent_duration_second} seconds."
                    )
        time.sleep(1)


username = input("Enter a name for your user account: ")
# login_time will be used to create the name of the csv file that will be generated
# login_time = datetime.now().strftime("%Y%m%d_%H:%M:%S")

# create a detectnet object instance that loads the 91-class SSD-Mobilenet-v2 model
# model string and threshold value can be different
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# create an instance of the videoSource object(openning camera stream)
camera = jetson.utils.videoSource("csi://0")

# create a video output interface with the videoOutput object and create a main loop that will run until the user exits(Display loop)
display = jetson.utils.videoOutput("display://0")

cat_watcher(username)  # call the above function
