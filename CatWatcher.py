#!/usr/bin/python3

"""
A real-time object detection program that uses a live camera feed to monitor a litter box for a cat...
The program records the cat's entry and departure times whenever he uses the litterbox in a CSV file.
It will also send email notifications to the user, if _email_alert() function is uncommented inside the the cat_watcher() function.

Dependencies:
- jetson.inference
- jetson.utils

Functions:
- cat_watcher: Monitors the litter box for the cat and sends notifications and records time data.
- _email_alert: Sends notifications to the user whenever the cat enters or leaves the camera's field of view.
- _record_data_in_csv: Records the time data of the cat's presence in a CSV file.

Usage:
To use the module, call the `cat_watcher` function with a username as an argument. The function will continuously monitor the camera until it is stopped manually. 

The function `_email_alert` is called by `cat_watcher` and should not be called directly. 
Similarly, `_record_data_in_csv` is also called by `cat_watcher` and should not be called directly.

Example:
>>> cat_watcher("username")
"""

from datetime import datetime, date
import time
import smtplib
import ssl
import csv
import logging
import os
import jetson.inference
import jetson.utils


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def _email_alert(recorded_time, duration):
    """
    Send notifications to the user whenever the cat enters or leaves the camera sight.
    Currently it's not secure as I have hardcoded password in my code and I have to lower gmail security level to make this work.
    An optimation is needed or notification should be sent using a different method.
    """
    from dotenv import load_dotenv
    port = 465
    context = ssl.create_default_context()

    # Load key-value pairs from .env file into environment variables
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")

    if duration == 0:
        message = f"""\
		Subject: Cat-LitterBox Alert


		Hey you! It's {recorded_time} now.
		Your cat is in the litterbox!"""
    else:
        message = f"""\
		Subject: Cat-LitterBox Alert


		Hey again!
		Your cat left the litterbox at {recorded_time}.
		He used the toilet for {duration}."""

    # create a secure connection with Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(sender_email, sender_email_password)
            server.sendmail(sender_email, receiver_email, message)
        except smtplib.SMTPAuthenticationError:
            logger.error("Email not working due to authentification error.")
        except OSError:
            logger.error("Email not working due to OS error.")


def _record_data_in_csv(
    user_name: str,
    entry_timestamp_epoch: float,
    depart_timestamp_epoch: float,
    toilet_duration: float,
):
    """
    Record time data to the csv file

    :param user_name: the user name entered by the user
    :param entry_timestamp_readable: the time when the cat enters the litterbox
    :param depart_timestamp_readable: the time when the cat departs the litterbox
    :param toilet_duration: the duration of the cat at the litterbox
    """
    date_of_the_day = date.today()
    entry_timestamp_readable = datetime.fromtimestamp(entry_timestamp_epoch).strftime(
        "%Y%m%d_%H:%M:%S"
    )
    # Name of the csv file is the combination of the username and the entry time
    local_user = os.getenv("USER")
    path_to_csvfile = (
        f"/home/{local_user}/cat_watcher_output/{user_name}{entry_timestamp_readable}"
    )
    logger.info("The path of the csv file is %s", path_to_csvfile)
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


def cat_watcher(user_name: str) -> None:
    """
    A continous monitoring system is enabled by using a camera to detect the presence or absence of a cat in a litterbox.
    It sends notifications to the user when the cat shows up or leaves the litterbox and records the timestamps in a CSV file.

    :param user_name: a string representing the name for the user account.
    """
    max_absent_time = 15
    cat_absent_duration_second = 0
    entry_timestamp_epoch = None

    while True:
        cat_is_here = False
        # Capture the next video frame from the camera
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
                break
        
        if cat_is_here:
            if entry_timestamp_epoch is None:
                # cat first shows up
                entry_timestamp_epoch = time.time()
                # Send email alert of cat showing up at litterbox
                # _email_alert(entry_timestamp_readable, 0)
            else:
                # cat has showed up earlier
                if -1 < cat_absent_duration_second <= max_absent_time:
                    # Set cat_absent_duration_second to 0 if cat shows up again within 15 secs.
                    cat_absent_duration_second = 0
                else:
                    logger.error(
                        "The cat's absence time has an invalid value of %d seconds.", cat_absent_duration_second
                    )
        else:
            if entry_timestamp_epoch is not None:
                if cat_absent_duration_second < max_absent_time:
                    cat_absent_duration_second += 1
                    logger.info(
                        "Emma, your cat has not been seen in the litterbox for %d seconds", cat_absent_duration_second
                    )
                else:
                    # If cat is absent for more than 15 seconds, the program determines that the cat has left the litter box
                    depart_timestamp_epoch = time.time() - max_absent_time
                    toilet_duration = depart_timestamp_epoch - entry_timestamp_epoch
                    # Send email alert of cat leaving the litterbox
                    # _email_alert(depart_timestamp_readable, toilet_duration)
                    logger.info("Recording data...")
                    _record_data_in_csv(
                        user_name,
                        entry_timestamp_epoch,
                        depart_timestamp_epoch,
                        toilet_duration,
                    )
                    # Reset
                    entry_timestamp_epoch = None
                    cat_absent_duration_second = 0
        time.sleep(1)


username = input("Enter a name for your user account: ")

# create a detectnet object instance that loads the 91-class SSD-Mobilenet-v2 model
# model string and threshold value can be different
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# create an instance of the videoSource object(openning camera stream)
camera = jetson.utils.videoSource("csi://0")

# create a video output interface with the videoOutput object and create a main loop that will run until the user exits(Display loop)
display = jetson.utils.videoOutput("display://0")

cat_watcher(username)
