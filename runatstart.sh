#!/bin/bash
env HOME=/home/pi
vncserver -kill :1
vncserver 
cd /home/pi/rapiro/
# python webmain.py
python htmlvoice.py
