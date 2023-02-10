# CatWatcher Program Edited on 20230210
## What does this program do?
The program uses image recognition to monitor the cat and logs the data whenever the cat uses the litterbox. To be more specific:
- A camera is constantly running in front of a litterbox.
- Upon a cat being caught on camera, an email notification is sent to user (optional, not activated now).
- Upon cat leaving the sight of camera, an email notification is sent to user (optional, not activated now).
- Output CSV files recording the times when a cat enters and exits the litterbox.

### Diagram of this program
![alt](https://github.com/emma-jinger/CatWatcher/blob/main/CatWatcher%20Program%20Diagram%20.png "Program Diagram")
### Output CSV File
***Note: Currently, each time entry is recorded in its own CSV file.*** <br>
The content of a sample file is shown as follows:
```
date,entry,depart,duration
2023-01-13,1673672546.8753567,1673672549.9890501,3.1136934757232666
```
- `date` is a `datetime.date()` object; `entry`, `depart`, and `duration` are `float`.
- The data is going to be loaded to a Postgres database. Before being loaded, `entry` and `depart` should be transformed to `datetime.datetime()` data type.

## Setup for the Program  
**Device used**: [The NVIDIA® Jetson Nano™ Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)<br>
**Library the Program Depends on**: [jetson-inference library](https://github.com/dusty-nv/jetson-inference)

## Possible Issues
- The camera/machine learning program can not always recognize the cat, depending on how the cat positions himself in the litterbox. This leads to missing data on the cat's bathroom behavior.
- The Nano device crashes/dies for unknown reasons. It is possibly related to limited memory and processing power of the Nano device.
## Future development
- Make this program a service
