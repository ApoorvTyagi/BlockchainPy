FROM python:3.7

RUN mkdir /code

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "/code/.py", "--port", "5000"]