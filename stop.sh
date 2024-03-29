pid=$(ps -ef | grep "rpi.py" | grep -v grep | awk '{print $2}')
killresult=$(ps -ef | grep "rpi.py" | grep -v grep | awk '{print $2}' | xargs kill 2>/dev/null)

if [ -z "$pid" ]
then
	echo -e "\nProcess is already stopped...\n"
else
	echo -e "\nKilled rpi.py [$pid]\n"
fi
