# TUIO2Socket.IO
Python script that receives TUIO events and converts them to Socket.IO events to be used in the browser.
tuioToSocketio.py is a script that opens a tuio cLient that listen for events, which are then proxied to the browser using Socket.IO.
Also implements a web server and calls chromium browser for easy termination.
socket-io.min.js is provided here for convinience
The rest of the files are modified from  WebGL fluid simulation by @PavelDoGreat (https://github.com/PavelDoGreat/WebGL-Fluid-Simulation), most important mods are the section in script.js which receives Socket.IO events and translates to internal pointers.
