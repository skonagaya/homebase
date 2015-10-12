if [ -z "$(ps -ef | grep rpi.py | grep -v grep | awk '{print $3}')" ]
then
	echo -e "\nStopped\n"
else
	echo -e "\nRunning\n"
fi
