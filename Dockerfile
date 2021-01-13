FROM python:3.6
LABEL maintainer="nilaivemula@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 2222 80
ENTRYPOINT ["python"]
CMD ["app/app.py"]
