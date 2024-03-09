FROM python:3.11

WORKDIR /app

COPY ./python/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./python/main.py /app/main.py
COPY ./python/post.py /app/post.py
COPY ./python/get.py /app/get.py

ENV FLASK_APP=/app/main.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
