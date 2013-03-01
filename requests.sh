#start_date=`date +"%Y-%m-%dT%H:%M:%SZ"`
for i in `seq 0 2`;do
	word=$(sed `perl -e "print int rand(99999)"`"q;d" /usr/share/dict/words | sed "s/'//g" ); 
	curl  http://$1.compute-1.amazonaws.com:8000/fortune/$word 
done

to=`date +"%Y-%m-%dT%H:%M:%SZ"`
sleep 1

echo $from $to;
from=`date -v -10S +"%Y-%m-%dT%H:%M:%SZ"`
curl -u ohmy@uic.edu:Hohoho "https://api.sumologic.com/api/v1/logs/search?q=error&from=$from&to=$to&tz=CST&format=text"
