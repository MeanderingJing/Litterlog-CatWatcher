# CatWatcher Program Edited on 20230210
## What does this program do?
**The main purpose of this program is to record the times when a cat uses the litterbox.** To be more specific:
- A camera is constantly running in front of a litterbox.
- Upon a cat being caught on camera, an email notification is sent to user (optional, not activated now).
- Upon cat leaving the sight of camera, an email notification is sent to user (optional, not activated now).
- Output CSV files recording the times when a cat enters and exits the litterbox.

*Note: Currently, each time entry is recorded in its own csc file. The content of a sample file is shown as follows:*
```
date,entry,depart,duration
2023-01-13,1673672546.8753567,1673672549.9890501,3.1136934757232666
```
## What device do I use to run this program?  
**Device used**: [The NVIDIA® Jetson Nano™ Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)<br>
**Dependent**: [jetson-inference library](https://github.com/dusty-nv/jetson-inference)


