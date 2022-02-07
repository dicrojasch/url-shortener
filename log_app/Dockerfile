FROM python:3.9.10

RUN pip install --upgrade pip
COPY . /log_app
WORKDIR /log_app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "log_app.py"]
