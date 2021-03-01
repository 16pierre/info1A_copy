FROM python:alpine
COPY src /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["gunicorn", "--workers=1", "--bind", "0.0.0.0:80", "main:app"]
