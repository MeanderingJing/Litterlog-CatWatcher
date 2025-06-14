# CatWatcher Program Edited on 20230531
## Setup for the Program  
**Device used**: [The NVIDIA® Jetson Nano™ Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)<br>
**Library the Program Depends on**: [jetson-inference library](https://github.com/dusty-nv/jetson-inference)
<div align="center">
    <img src="https://github.com/emma-jinger/Litterlog-CatWatcher/blob/main/LitterLog_Hardware.jpg" alt="LitterLog Hardware" width="600" height="550">
</div>

## What does this program do?
The program uses object detection technology to monitor a cat's litterbox and logs the data whenever the cat uses the litterbox. To be more specific:
- A camera is constantly running in front of a litterbox.
- Upon a cat being caught on camera, an email notification is sent to user (optional, not activated now).
- Upon cat leaving the sight of camera, an email notification is sent to user (optional, not activated now).
- Output CSV files recording the times when a cat enters and exits the litterbox.

## How to use this program?
### Clone `jetson-inference` and build it from source
```
sudo apt-get update
sudo apt-get install git cmake libpython3-dev python3-numpy
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig
```
### Make a directory that the camera outputs data
`mkdir /home/$USER/cat_watcher_output`

### Make a `.env` file storing your personal info 
*This is not required at the moment as I didn't activate the sending email notification function in my code.*  
```
SENDER_EMAIL = type_in_your_sender_email
RECEIVER_EMAIL = type_in_your_receiver_email
SENDER_EMAIL_PW = type_in_password
```
### Install dotenv package 
*This is not required at the moment as I didn't activate the sending email notification function in my code.* 
```
pip3 install dotenv
```

### Run the program
Go to the directory where this repo is, and execute the command:
``` 
python3 CatWatcher.py
```
## Output CSV File
***Note: Currently, each time entry is recorded in its own CSV file.*** <br>
The content of a sample file is shown as follows:
```
date,entry,depart,duration
2023-01-13,1673672546.8753567,1673672549.9890501,3.1136934757232666
```
- `date` is a `datetime.date()` object; `entry`, `depart`, and `duration` are `float`.
- The data is going to be loaded to a Postgres database. Before being loaded, `entry` and `depart` will be transformed to `datetime.datetime()` data type.


## Possible Issues
- The camera/machine learning program can not always recognize the cat, depending on how the cat positions himself in the litterbox. This leads to missing data on the cat's bathroom behavior.
- The Nano device crashes/dies for unknown reasons. It is possibly related to limited memory and processing power of the Nano device.
## Future development
- Develop my own Object Detection program that does not depend on the `jetson-inference` library.
- Fix the program executing issue on headless mode
- Make this repo into a Python package, which contains the python module as well as requirements and documentation. 
- Make this program a service, and have a default username if none is supplied.


