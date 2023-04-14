FROM python:3
LABEL description="pavelpetrcz/ppetr"
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . code
WORKDIR /code
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]