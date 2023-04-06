FROM python:3
LABEL description="pavelpetrcz/ppetr"
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD python