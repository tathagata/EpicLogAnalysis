# Epic Operational Analysis Battle: SumoLogic vs Splunk Storm


How beneficial is opeartional analytics? While I do understand the help to DevOps, what benefit does it bring to 
the business and more importantly the customer? It surely must be beneficial as this space is as crowded as the 
bazars of India - Splunk is probably the most well known company, but companies like SumoLogic, PaperTrail, Loggly,
Logarythm, and even the free and open source alternative Logstash are being heavily used and many of them deifnitely have 
paying customers.

I looked around for some data to compare them, but there was nothing good. So, I started to test them out. I begin with SumoLogic
and Splunk Storm, and hopefully will test out loggly and logstash soon.

I really wanted to understand hoopla behind what appears to be a mere combination of ftp, map-reduce, and search of log/text files
and signed up for the free options. Before we go into the tech side, lets define the business problem.


### Business Idea: Fortune Cookie quote as a web service  
Lets say I run a business where I provide a fortune cookie quote based on a search text. Its hard to imagine, anybody
will pay for such a service, but lets say somehow we have growth-hacked thousands of users.

### Business Questions we want to answer
* What % of queries are being replied with a quote? If this is too low we need to invest in generating more quotes?
* How often are we repeating the same quotes?
* How much load can we serve?

### Replicating an enterprise set up
I worked briefly mainitaining ugly enterprise software which had grown organically over years with numerous different systems talking to each
other and spewing numerous lines of logs. Whenever systems would go down - we had to login to multiple severs, look through the 
log files and troubleshoot the outages. Once detected, we wrote bandaid scripts that would monitor systems for failure and generate 
alerts or restart severs/services.

### EC2 servers
So how do I replicate such an enterprise level system? Certianly impossible in my old laptop. So we go to the cloud. 

I have been working on building a django/Backbone.js app with a friend of mine to help recruiters and candidates connect quickly at career fairs.
And we started to experiment with EC2 micro instances. I'm by no means a cloud expert, but the pleasure of having a sudo-able command line makes life 
easy.

I took a simple ubuntu-precise-12.04-amd64-server image and added the port 8000 to the secruity group. Then just spawn 10 instances of the same.
There are command line utils for controlling ec2 instances, but for my purpose I chose not to delve into them. 


### The server
For the web server, we use a micro-framework called bottle.py - and all we have there is a call to the shell utility fortune.
It couldn't be simpler than this.
    

So if I make a call to the url 

    curl http://ec2instance.com 

I'm supposed to get back a response.`

### Testing the server
While Apachebench is a great tool for load testing web severs, what I needed was to test urls with multiple parameters. Turns out,
there isn't a good way to do that in ab. So we have to roll our sleeves a bit and get write something similar

To mimick a random word search from our user, we generate a random word and curl the web url for each instance.

    word=$(sed `perl -e "print int rand(99999)"`"q;d" /usr/share/dict/words | sed "s/'//g" );
    curl  http://$1.compute-1.amazonaws.com:8000/fortune/$word
 
Add this to the wonderful utility GNU parallel and you have a DDOS weapon.
    parallel sh -c ./requests -- `seq 20000`

However, sometime down the line, I realized I needed something more structured than bash files and have started with getlatency.py.
So we make a request to our web servers and use the time stamp from the HTTP response header to query SumoLogic API. That will give us a sense of how realtime SumoLogic service is.

### Install agents 
To siphon out your data to the cloud for analytics we need to have some agents who will securely remote copy the files out of your
servers to the data centers of your service provider. SumoLogic alls them collectors and Splunk calls them forwarders - but the basic 
idea is pretty much the same. 

Since we are replicating a moderate deployment we need to have a way to automatically deploy our mini web app and the agents which will 
report the performance tests that we will conduct.

### Deploying SumoLogic with SumoLogic.sh 
While pretty self explanatory, what this script does is to login to all the amazon instances we have from saved in instances file and
deploys our mini-web app. Then it uploads the agents and does an unattended installation. The SumoLogic documentation is super-friendly
and I was done scripting the entire thing in one afternoon.

* config.json - Tells the collector where to look into for log files
* genconf.sh - Genconf is meant to generate key-value pair files that the sumologic installer will use for registering the collector at the time of the installation. Since I'll be deploying to a bunch of servers, this file helps automate the generation of those files.
  


### Deploying Splunk Storm with Storm.sh



### Realtime analysis
How real time are the two services really? That in my mind is really the acid test. 

### SumoLogic Test Results



### Splunk Storm Test Results


### Metrics to measure business problem

To measure how we are serving our customers we define the following metrics

* Number of returned fortunes/Number of queries
	Based on my initial numbers, the default fortune database is really bad.

* Latency of Map of the client requests
	I plan to use a bunch of proxies to test this idea. 

* More to comes


(Test results)









