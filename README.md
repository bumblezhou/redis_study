# redis_study

## A simple project to demo how to use redis for document storage and full-text search.

## Load from docker:
```bash
docker run -p 6379:6379 --name redis_stack_server redis/redis-stack-server:latest
```

## Install python and required libs:
```bash
sudo apt install python3 -y
sudo apt install python3-pip -y
pip install -r requirements.txt
```