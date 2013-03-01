

## Epic Operational Intelligence Battle: SumoLogic vs Splunk Storm vs Loggly vs Logstash vs ...

(WORK IN PROGRESS - like everything else in life)

What is operational intelligence?

_Operational intelligence (OI) is a category of real-time dynamic, business analytics that delivers visibility and insight into data, streaming events and business operations. Operational Intelligence solutions run queries against streaming data feeds and event data to deliver real-time analytic results as operational instructions. Operational Intelligence provides organizations the ability to make decisions and immediately act on these analytic insights, through manual or automated actions._

Yes, that's Wikipedia verbatim! So who do you think would be most happy with this?

<img src="http://www.technologyreview.com/blog/mimssbits/files/77798/devops_borat.png"> 

Definitely this guy. _Chinqui!_
 
I worked briefly in IT maintaining ugly enterprise software which had grown organically over the years with disparate systems talking to each
other and spewing numerous lines of logs. Whenever systems would go down - we had to login to multiple servers, look through the 
log files and troubleshoot the outages. Once detected, we wrote band-aid scripts to fix problems, scripts that would monitor systems for failure and generate alerts or restart servers/services.


While I do understand the help to DevOps, what benefit does it bring to 
the business? And more importantly, the customer? There must be some benefits as the space is as crowded as the 
bazars of India - Splunk is probably the most well known, but companies like SumoLogic, PaperTrail, Loggly,
Logarythm, and even the free and open source alternative Logstash are being heavily used and many of them definitely have 
paying customers.


### Business Idea: Fortune Cookie quote as a web service  
Lets say I run a business where I provide a fortune cookie quote based on a search text. Its hard to imagine, anybody
will pay for such a service, but lets say somehow we have _growth-hacked_ thousands of users.

### Business Questions we want to answer
* What % of queries are being replied with a quote? If this is too low, do we need to invest in generating more quotes?
* How often are we repeating the same quotes?

### Tech questions 
* How much load can we serve? Can we avoid downtime by minining log data?
* How does changing log messages due to code change or an upgrade of some software to a new version effect search results?


### Replicating an enterprise set up on EC2
So how do I replicate such an enterprise level system? Certainly impossible in my old laptop, So we go to the cloud. I'm by no means a cloud expert, but the pleasure of having a sudo-able command line makes you feel right at home.

I took a simple ubuntu-precise-12.04-amd64-server image and added the port 8000 to the security group. Then just spawn 10 instances of the same ami.
There are command line utilities for controlling ec2 instances, may be I'll incroporate them at a later stage. 


### The server
For the web server, we use a micro-framework called bottle.py - and all we have there is a call to the shell utility fortune.
It couldn't be simpler than this.
    

So if I make a call to the url 

    ```bash
    curl http://ec2-23-22-126-243.compute-1.amazonaws.com:8000/fortune/apple
    ``` 
I'm supposed to get back a response.`

	We were young and our happiness dazzled us with its strength.  But there was
	also a terrible betrayal that lay within me like a Merle Haggard song at a
	French restaurant. [...]
		I could not tell the girl about the woman of the tollway, of her milk
	white BMW and her Jordache smile.  There had been a fight.  I had punched her
	boyfriend, who fought the mechanical bulls.  Everyone told him, "You ride the
	bull, senor.  You do not fight it."  But he was lean and tough like a bad
	rib-eye and he fought the bull.  And then he fought me.  And when we finished
	there were no winners, just men doing what men must do. [...]
		"Stop the car," the girl said.
		There was a look of terrible sadness in her eyes.  She knew about the
	woman of the tollway.  I knew not how.  I started to speak, but she raised an
	arm and spoke with a quiet and peace I will never forget.
		"I do not ask for whom's the tollway belle," she said, "the tollway
	belle's for thee."
		The next morning our youth was a memory, and our happiness was a lie.
	Life is like a bad margarita with good tequila, I thought as I poured whiskey
	onto my granola and faced a new day.
			-- Peter Applebome, International Imitation Hemingway
			   Competition







### Testing the server
While Apachebench is a great tool for load testing web severs, what I needed was to test urls with multiple parameters. Turns out,
there isn't a good way to do that in ab. So we have to roll our sleeves a bit and get write something similar

To mimic a random word search from our user, we generate a random word and curl the web url for each instance.

    ```bash
    word=$(sed `perl -e "print int rand(99999)"`"q;d" /usr/share/dict/words | sed "s/'//g" );
    curl  http://$1.compute-1.amazonaws.com:8000/fortune/$word
    ``` 

Add this to the wonderful utility GNU parallel and you have a DDOS weapon.
    
    ```bash
    parallel sh -c ./requests -- `seq 20000`
    ```

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

* _config.json_ - Tells the collector where to look into for log files
* _genconf.sh_ - Genconf is meant to generate key-value pair files that the sumologic installer will use for registering the collector at the time of the installation. Since I'll be deploying to a bunch of servers, this file helps automate the generation of those files.
  


### Deploying Splunk Storm with Storm.sh
(coming soon)


### Realtime analysis
How real time are the two services really? That in my mind is really the acid test. 
(coming soon)


### SumoLogic Test Results
(coming soon)


### Splunk Storm Test Results
(coming soon)

### Metrics to measure business problem
<img src='https://dl.dropbox.com/u/18146922/SumoLogicDashBoard.png'>

To measure how we are serving our customers we define the following metrics

* Number of returned fortunes/Number of queries
	Based on my initial numbers, the default fortune database is really bad.

* Latency of Map of the client requests
	I plan to use a bunch of proxies to test this idea. 

* More to come


