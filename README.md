#### Project ID: PW19KP001
### Team Members
* [**Gagan C J**](https://github.com/GaganCJ)
* **Rakshith K S**
#### Project Guide: Kiran P
<hr>

# Student Attendance System using Face Recognition

## Abstract
**Student Attendance System** deals with the recording and organizing of the student's attendance details. It generates the attendance of the student using face recognition technique.

This project is built as a part of final year project.

## Getting Started with Prerequisites

- Step 1 : Install [pip](https://pip.pypa.io/en/stable/installing/) for Python 3.5+
- Step 2 : Clone this repository.
- Step 3 : Install [virtualenv for python3](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv/).
    - Instead of <code>python</code>, use <code>python3</code>
- Step 4 : Create virtualenv folder in the root folder.
```
python3 -m virtualenv foldername
```
- Step 5 : Install Prerequisite packages from pip (If your system is running on Debian/Ubuntu, please search for the instructions for installing in Windows 7 or above System).
```
source foldername/bin/activate
pip3 install Flask dlib opencv-python-contrib face-recognition imutils
```
**OR**
```
source foldername/bin/activate
python3 -m pip install Flask dlib opencv-python-contrib face-recognition imutils
```
### Running the Application

Run this code in Virtual Environment from the root folder
```
source foldername/bin/activate
flask run
```
To exit from Virtual Environment
```
deactivate
```

## Running the tests

For now, The idea of testing as not been planned.

## Built With

* [Metro 4 CSS UI](https://metroui.org.ua/) and [jQuery](https://jquery.com/) - A Stylish Framework.
* [Flask](http://flask.pocoo.org/) - A web development server-side framework built on python.
* [OpenCV](http://opencv.org) - OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial products. Being a BSD-licensed product, OpenCV makes it easy for businesses to utilize and modify the code.
* [dlib](http://dlib.net) - Modern Deep Learning toolkit containing machine learning algorithms and tools for creating complex software to solve real world problems.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg1MDAxNDM4OF19
--># FP-L-I-330-OpenCV
