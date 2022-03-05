FROM python:3.9.7

ENV PYTHONUNBUFFERED 1
COPY . /home/yserediu/app/
WORKDIR /home/yserediu/app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000