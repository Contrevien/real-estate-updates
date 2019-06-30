FROM python:3
RUN pip install flask flask-restful
ADD . /code
WORKDIR /code
EXPOSE 5000
CMD python app.py