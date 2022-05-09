#!/bin/bash

~/.fehbg
xfce4-power-manager &
pamac-tray &
pasystray &
blueberry-tray &
nm-applet &
picom --experimental-backends --corner-radius 0 -o 0.5 -b
