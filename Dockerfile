FROM python:buster
RUN apt update && apt install -y tini
RUN mkdir -p /app
ADD ./ /app
WORKDIR /app
RUN pip install -r ./requirements.txt

ENTRYPOINT ["tini", "--"]
CMD ["python ./main.py"]
