FROM python:3.8.5

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x run.sh
CMD ./run.sh