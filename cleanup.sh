#!/bin/bash
# find /home/pi/Linus_Timelapse -name "*.jpg" -mtime +5 -exec rm -rf {} \; # older than 5 days
find /home/pi/Linus_Timelapse -name "*.jpg" -mmin +60 -exec rm -rf {} \; # older than 60 minutes
# find /home/pi/Linus_Timelapse/trash -name "*.jpg" -mmin +120 -exec rm -rf {} \; # older than 120 minutes
