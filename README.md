# Breaker
### Welcome to Breaker!
### Breaker is a program created by Rishik Buneti which uses Artificial Intellegence to help the user allocate times for computer usage and breaks. 

# Overview
### Do you or someone you know spend an unhealthy amount of time in front of a computer screen? If so, then this program is your savior. Breaker is a program that uses Artificial Intellegence to tell when a user is in front of the computer screen, and periodically remind them to get up and take a break. 

# How it works
### When the program is run, the camera is open and uses facial recognition from haarcascades to identify the user. Each second that a face is recognized the program updates a counter to count how long the user has been in front of the computer. After the set time is completed (the default time set is 20 min), the program both prints and speaks to the user about whether or not they can continue their computer usage. This decision is made by comparing to the number of frames in which a face is present to the number of total frames. If the user is present in more than 75% of all frames, then the program asks them to take a break from the computer. (Variables and constants can be changed to fit the users needs).

# Accessibility 
### This code can be run in several different ways. Initially, it was solely meant for the Jetson Nano (a mini computer similar to the raspberry pi which was designed specifically for Artificial Intellegence and Machine Learning), however for easier accessibility for potential users, I created a far simpler version which can be run almost anywhere. The Jetson Nano specified code requires a flashed SD card, a machine, webcam, cables, and significantly more package installations, however has a much simpler code. On the other hand, the generalized version has far better versatility, but its code is much more complex, concurrenlty using multiple coding languages to function.  

# If you're attempting to recreate the entire code for yourself, either for understanding or learning purposes, I recommend using the file for the Jetson Nano and running it through a code editor (I used Visual Studio Code). 

# If you're just planning on running the code and testing it out, feel free to copy the code into your own code editor, or using my google colab with the link below. 
https://tinyurl.com/Shikuri-Breaker

# Inspiration:
### My parents who always nagged me about too much time on the computer. As someone a modern teen who enjoys programming, staying away from the computer is a difficult task which comes with several drawbacks. That's why, I decided to create this program to help anyone who has similar problems.
