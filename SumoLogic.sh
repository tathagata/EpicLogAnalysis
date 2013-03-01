#!/bin/bash
./genconf.sh


for i in `cat instances`;do	
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'sudo apt-get install python-bottle fortune'
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'mkdir logs app sumo storm'

	#start python sever
	scp -i ~/.ssh/Setup.pem fortune.py ubuntu@$i.compute-1.amazonaws.com:/home/ubuntu/app/fortune.py
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'cd /home/ubuntu/app/; nohup python fortune.py > foo.out 2> foo.err < /dev/null &'


	#upload sumo config and deb
	scp -i ~/.ssh/Setup.pem config.json ubuntu@$i.compute-1.amazonaws.com:/home/ubuntu/sumo/config.json
	scp -i ~/.ssh/Setup.pem confs/sumo-$i.conf ubuntu@$i.compute-1.amazonaws.com:/home/ubuntu/sumo/.
	scp -i ~/.ssh/Setup.pem sumocollector_19.30-4_amd64.deb ubuntu@$i.compute-1.amazonaws.com:/home/ubuntu/sumo/.

	#install and start sumo
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'cd sumo;sudo cp *.conf /etc/sumo.conf; sudo dpkg -i sumocollector_19.30-4_amd64.deb'
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'sudo /etc/init.d/collector start'

	#clean up sumo
	sleep 1	
	ssh -l ubuntu -i ~/.ssh/Setup.pem $i.compute-1.amazonaws.com 'sudo rm /etc/sumo.conf; rm /home/ubuntu/sumo/*.conf'
done

rm confs/*.conf
