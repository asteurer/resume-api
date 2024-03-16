# Overview

- This is a containerized REST API that gets and posts resume data to a PostgreSQL database using Python Flask. 

# Usage

- On a host running Linux OS, run the following commands to install Docker and Docker Compose:

```
sudo yum update -y
sudo yum install docker -y
sudo service docker start 
sudo usermod -aG docker ec2-user
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- Navigate to the directory you want the Docker Compose file and run the following command to install: 

```
sudo curl -L https://github.com/asteurer/resume-api/raw/master/compose.yaml -o compose.yaml
```

- In the same directory, create a .env file that contains the following credentials: 
    - DATABASE_HOST (this should equal "db")
    - DATABASE_USER
    - DATABASE_PASSWORD
    - VALID_TOKEN (this is the token that will validate insert and update requests)

```
echo "DATABASE_HOST=${YOUR_VARIABLE_HERE}" > .env
echo "DATABASE_USER=${YOUR_VARIABLE_HERE}" >> .env
echo "DATABASE_PASSWORD=${YOUR_VARIABLE_HERE}" >> .env
echo "VALID_TOKEN=${YOUR_VARIABLE_HERE}" >> .env
```

- Once the .env file is created, run the below command: 

```
sudo docker-compose up -d
```

- The containers are now running. You can access the API via CURL request as shown below:

```
# To get the resume data:
curl -o outputfile.json http://YOUR_HOST_HERE:5000/api/resume/get

# To insert/update the resume data:
# An example for how the resume data is structured can be seen here: https://github.com/asteurer/resume-api/blob/master/data.json
curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_VALID_TOKEN" \
    -d @Path/To/data.json \
    'http://YOUR_HOST_HERE:5000/api/resume/update'
```