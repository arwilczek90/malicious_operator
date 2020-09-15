FROM python:buster
RUN apt update && apt install tini
RUN mkdir -p /app
ADD ./ /app
WORKDIR /app
RUN pip install ./requirements.txt

ENTRYPOINT ["tini", "--"]
CMD ["python main.py"]
