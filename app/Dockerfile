FROM python:3.9.10

ENV FLASK_APP=app
ENV FLASK_ENV=development
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
