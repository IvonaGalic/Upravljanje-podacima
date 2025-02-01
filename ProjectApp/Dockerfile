FROM python:3.10

WORKDIR /home/app/
COPY . /home/app/
RUN pip install -r ./requirements.txt

RUN apt-get update && apt-get install -y curl
RUN curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

CMD ./wait-for-it.sh mysql:3306 -- ./wait-for-it.sh redis:6379 -- uvicorn main:app --host 0.0.0.0 --port 5000