FROM python:3.12.2

RUN mkdir /linklist

WORKDIR /linklist

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /linklist/docker/*.sh

CMD python manage.py migrate