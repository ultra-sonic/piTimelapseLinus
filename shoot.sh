export LD_LIBRARY_PATH=/opt/vc/lib
DAY=`date +"%Y%m%d"`
DATE=`date +"%Y%m%d_%H%M%S"`
TYPE="jpg"
FILENAME="/home/pi/Linus_Timelapse/$DAY/Linus_Timelapse_$DATE.$TYPE"


FREESPACE=`df $PWD | awk '/[0-9]%/{print $(NF-2)}'`
THRESHOLD=200000 # 200MB

if [ $FREESPACE -gt "$THRESHOLD" ]; then 
	if [ ! -d `dirname $FILENAME` ]; then
		mkdir `dirname $FILENAME`
	fi

	# --roi	: Set region of interest (x,y,w,d as normalised coordinates [0.0-1.0]) // upper left is origin 0,0
	raspistill -o $FILENAME -e $TYPE -q 100 # -roi 0.3,0.05,0.6,0.8 #  -w 1837
	echo $FILENAME
	pgrep rsync
	if [ $? = 1 ]; then 
		echo "no rsync runnning"
		rsync -av -e "ssh" /home/pi/Linus_Timelapse/$DAY/ omarkowski@192.168.9.3:/data_100G/Linus_Timelapse/$DAY/
	else
		echo "skipping  rsync - already running"
	fi
else
	echo "Not enough space left on device!";
fi
