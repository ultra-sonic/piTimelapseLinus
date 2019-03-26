export LD_LIBRARY_PATH=/opt/vc/lib
/opt/vc/bin/raspivid -t 0 -w 1280 -h 720 -hf -ih -fps 20 -o - | nc -k -l 2222
