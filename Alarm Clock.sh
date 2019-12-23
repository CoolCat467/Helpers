#/bin/bash
# Simply an alarm clock

function alarm {
	omxplayer -o both --vol 2000 /home/pi/Desktop/Other/Alarm\ Clock/Alarm\ clock\ beeps.wav > /dev/null
	alarm
}

function main {
	$(python3 /home/pi/Desktop/Other/Alarm\ Clock/alarm\ clock.py)
	alarm
}

main