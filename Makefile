send_request:
	start_date=$(shell date +"%Y-%m-%dT%H:%M:%SZ");\
	./requests.sh ec2-23-22-126-243; \
	end_date=$(shell date +"%Y-%m-%dT%H:%M:%SZ");\
	echo $$start_date $$end_date;\
	curl -u My@Email.edu:MySecretPassword "https://api.sumologic.com/api/v1/logs/search?q=error&from=$$start_date&to=$$end_date&format=text"


