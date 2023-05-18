FROM python:3

ENV DEBUG_MODE $DEBUG_MODE
ENV BASE_URL $BASE_URL
ENV DJANGO_SECRET $DJANGO_SECRET
ENV B_JWT $B_JWT
ENV DEFAULT_BLOGPOST_IMG $DEFAULT_BLOGPOST_IMG

LABEL description="pavelpetrcz/ppetr"
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . code
WORKDIR /code
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["python manage.py migrate"]
CMD ["runserver", "0.0.0.0:8000"]