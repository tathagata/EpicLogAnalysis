rm confs/*
for i in `cat instances`;do
	echo 'name='$i > confs/sumo-$i.conf
	echo 'email=someemail@gmail.com' >> confs/sumo-$i.conf
	echo 'password=VerySecret' >> confs/sumo-$i.conf
	echo 'sources=/home/ubuntu/sumo/config.json' >> confs/sumo-$i.conf
done
