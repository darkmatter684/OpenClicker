## OpenClicker

A MacOS autoclicker with an easy CPU load<br>
![image](https://user-images.githubusercontent.com/105139789/177389541-377b0a07-c01e-4050-a310-5ff8aef7cf20.png)<br>

### Introduction

OpenClicker beings the power of native windows autoclickers to MacOS<br>

### Features / Customization

1. Configure amount of clicks
2. Configure delay between clicks
3. Configure keybinds to start and stop clicking
4. Option to keep app above apps
5. Options to set keybinds locally or set them to work on every app (this requires root access, see below for more information)
6. Option to turn on notifications

## Installation

You can download the latest release: [here](https://github.com/darkmatter684/OpenClicker/raw/gh-pages/OpenClicker-x64.zip)

## Setup 

To setup the application:

Go to ``System Preferences > Secruity & Privacy > Privacy > Accessibility``<br>
Once you are here, press the lock to unlock the menu, and then add OpenClicker to the list of apps.<br>

To do this:<br>
![image](https://user-images.githubusercontent.com/105139789/177392661-133d37aa-9729-4cc0-8795-fe4f886ee91a.png)<br>
Press the + and then go to the location of the OpenClicker app<br>

Done!

## Notes

#### Global keybinds
These are a bit more complicated to get working.

To do this we want to give the app root access, which we can do through the ``sudo`` command in Terminal.<br>

Steps to get these working:
1. Go to the location of the application
2. Right click the app and press ``Show package contents`` <br><img width="258" alt="image" src="https://user-images.githubusercontent.com/105139789/177393696-d93c3d52-77b1-4e8c-be52-e9c91714f725.png">
3. Navigate to ``Contents > MacOS``
4. Open Terminal and type in ``sudo `` (sudo with a space after it) <br> ![image](https://user-images.githubusercontent.com/105139789/177394161-3fef73a6-3d26-4069-ac02-032b247f6f36.png) 
5. Drag the file titled "OpenClicker" into Terminal, it should look something like this <br>![image](https://user-images.githubusercontent.com/105139789/177394586-e0e2ad4f-0f9b-473a-b284-e3071e9a9e07.png)
6. Enter your passcode
7. Done! Global keybinds will now work! 
If you get "command not found" make sure you spelling is correct and make sure you put a space after sudo and before the path to the file

#### What I learned from this project

<p>OpenClicker was a really fun app for me to code, because through this I learned the basics and benefits of Object Oriented Programming. Additionally, if you look on GitHub you could find a .json file, which was my way of creating a save file. The JSON file allows anything that is changed in the program (including cooridnates of where the app is) to be saved and the next time you open the application all of the configurations you set will be saved there. Furthermore, while creating the site (this) I learned more about Markdown script and how to use GitHub "professionally"





