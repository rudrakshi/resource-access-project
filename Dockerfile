FROM python:3.10-slim
ENV PATH /usr/local/lib/python3.10/site-packages:${PATH}
COPY . /src
WORKDIR /src
EXPOSE 8282 8484 5000
RUN pip install -r /src/requirements.txt