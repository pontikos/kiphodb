FILE="/tmp/dbproject-${USER}.pid"

case "$1" in
		start)
			echo Starting dbproject server
			#nohup should let program continue running even when we exit terminal
			nohup python manage.py runserver --noreload > dbproject.log &
			#Write process id to file
			echo $! > $FILE
			echo Process id written to $FILE
			 ;;
		stop)
			echo Stopping dbproject server
			kill -9 `cat $FILE`
			rm $FILE
			echo Process id file $FILE removed
			 ;;
		restart)
			sh $0 stop;sh $0 start
			 ;;
		*)
			 echo "Usage: $0 {start|stop|restart}"
			 exit 1
esac
exit 0

