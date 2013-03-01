import subprocess
from bottle import route, run
import logging, string, re

@route('/fortune/:word')
def fortune(word):
	logging.info('Received query for %s',word)
	word = word.replace(string.punctuation,'')
	cmd=["fortune","-aim",word]
	fortune_string=''

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	
	try:
		fortune_string = out.split('%')[-2].replace(word,'<strong>'+word+'</strong>')
		logging.info('Generated fortune:%s',fortune_string)
		return fortune_string

	except:
		if len(fortune_string)==0:
			logging.error('No fortune generated for %s',word)
			return 'No donuts for ',word

	if err is not None:
		logging.critical(err)

logging.basicConfig(filename='../logs/fortune.log',level=logging.DEBUG)
run(host='0.0.0.0', port=8000, reloader=True)
