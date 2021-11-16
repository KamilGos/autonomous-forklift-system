
<div align="center" id="top"> 
  <img src=images/MainwindowGUI.png  alt="MainwindowGUI" />
  &#xa0;
</div>

<h1 align="center"> Autonomous-Forklift-System
 </h1>

<p align="center">
  <img alt="Top language" src="https://img.shields.io/badge/Language-Python-green?style=for-the-badge&logo=appveyor">
  <img alt="Status" src="https://img.shields.io/badge/Status-done-green?style=for-the-badge&logo=appveyor">
    <img alt="Repository size" src="https://img.shields.io/github/languages/code-size/KamilGos/Autonomous_Forklift_System?style=for-the-badge">
</p>


<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#computer-gui">GUI</a> &#xa0; | &#xa0;
  <a href="#microscope-tests">Tests</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#technologist-author">Author</a> &#xa0; | &#xa0;
</p>

![Movie presenting working system](watch_me_speedx8.mp4)

<video width="320" height="240" controls>
  <source src="watch_me_speedx8.mp4" type="video/mp4">
</video>
<br>

## :dart: About ##

An application that run the autonomous forklift paletization aglorithms. Projekt was created for Engineering Thesis. It was fully completed. The last release of this application is available in this repository. Alication uses image processing (OpenCV library) to detect the position of Acuco markers. Based on the calculated positions of the forklift, pallets and the storage place, the trajectories for the truck are generated (mainly using Voronoi graph and Dijsktra algorithm). Then the module responsible for communication with the robot controls it, so the robot collects choosed pallets and puts them one on top of the other in the designated warehouse. 

## :computer: GUI ##
The interface was created using the PyQt5 and pyqtgraph libraries.The following elements are shown in the figure:
1. **Menu bar** - user can change the FPTV coefficient, communication port and baudrate.
2.  **Image transmission** - user can choose between three views. The first view displays the real image from the camera. View 2 displays
marked tags with their identifiers. The third view displays the trajectories for a robot and updates it with each move
robot (fig. 3.22). 
3. **Entering identifiers** - to start 
system, the user has to enter the robot ID and the pallet that the robot has
deliver to the storage area. 
4. **Parameters** - In the Module statuses table you can observe
camera, communication and navigation module status. The Warehouse table shows the status graphically storage place. The Parameters table shows in sequence: camera number (by default 1), COM port (COM14 by default), baud rate (9600 by default), ratio FPTV (25 by default), fault information, phase one status, phase two status, and the number of steps remaining to complete the phase. 
5. **Start and progress** button that starts the palletization process (Start). It is available only after the correct robot and pallette identifiers are entered

## :microscope: Tests ##
1. **Correctness of generated paths** - The correct route is considered to be a safe route to the destination. In the first phase the palette is the goal. The robot has to reach the pallet and then pick it up. In the second phase
the goal is the storage area (warehouse). **Result: Correct**
<p align="center">
  <img src=images/test1t1.png width="350" />
  <img src=images/test1t2.png width="350" />
</p>

2. **Correctness of completing the route** - A correctly covered route is characterized by a minimal error between generated route and the route taken by the robot. This is equivalent to maintenance
safety assumptions for every traffic. **Result: Correct**
<p align="center">
  <img src=images/test1p1.png width="350" />
  <img src=images/test1p2.png width="350" />
</p>

1. **Correctness of multi-level storage** - This test checks whether the palletiser is correctly stacking the pallets. It is necessary to consider the created system as a multi-level palletizing system. **Result: Correct**
<p align="center">
  <img src=images/test4p2.png width="250" />
  <img src=images/test4p4.png width="250" />
  <img src=images/test4p6.png width="250" />
</p>

<p align="center">
  <img src=images/3paletyint.png width="250" />
  <img src=images/3palety.png width="180" />
</p>

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/KamilGos/Autonomous_Forklift_System

# Access
$ cd Autonomous_Forklift_System

# Run the project
$ sudo python3 main.py
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.

## :technologist: Author ##

Made with :heart: by <a href="https://github.com/KamilGos" target="_blank">Kamil Goś</a>

&#xa0;

<a href="#top">Back to top</a>






