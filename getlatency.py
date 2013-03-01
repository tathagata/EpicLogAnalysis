import urllib2, base64, time
from datetime import datetime
from datetime import timedelta

#copied from http://brannerchinese.wordpress.com/2012/05/24/useful-python-time-formats-for-dealing-with-http-headers/
def make_iso8601_time_string(time_struct):
    '''Input struct_time and output an ISO 8601 time string'''
    return time.strftime('%Y-%m-%dT%H:%M:%S', time_struct)


def test_sumo(from_time,to_time):
	username='tdasgu2@uic.edu'
	password='SgGv3RigROT6'
	url = "https://api.sumologic.com/api/v1/logs/search?q=error&from="+from_time+"&to="+to_time+"&tz=GMT"
	print url
	#request = urllib2.Request("https://api.sumologic.com/api/v1/logs/search?q=error&from=2013-02-27T00:01:02&to=2013-02-27T23:00:00")
	request = urllib2.Request(url)	
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	results = urllib2.urlopen(request)
	for result in results:
		print result


def test_aws():
	request = urllib2.Request("http://ec2-23-22-126-243.compute-1.amazonaws.com:8000/fortune/somethign")
	result = urllib2.urlopen(request)

	http_header_time =  result.info().__dict__['headers'][0].replace('Date: ','').replace('\r\n','')
	to_time = make_iso8601_time_string(time.strptime(http_header_time, '%a, %d %b %Y %H:%M:%S GMT'))
	
	http_header_time_ = datetime.strptime(http_header_time, '%a, %d %b %Y %H:%M:%S GMT')
	from_time = http_header_time_ - timedelta(seconds=60)
	
	print  "From:",from_time.isoformat(), "To:",to_time
	test_sumo(from_time.isoformat(),to_time)

if __name__ == "__main__":
	test_aws()
