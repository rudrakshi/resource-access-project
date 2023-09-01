## Prerequisites
- Python 3

## Clone the project
```
git clone https://github.com/rudrakshi/resource-access-project.git
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run API server
```
uvicorn api.resource_api:api --host 0.0.0.0 --port 8282
```

### Run Gateway server
```
uvicorn gateway.gateway_api:gate --host 0.0.0.0 --port 8484
```

### Run Consumer server
```
flask --app consumer.consumer_app run --host 0.0.0.0 --port 5000
```

### Run test
```
pytest
```

## API documentation (provided by Swagger UI)

[Resource API](http://127.0.0.1:8282/docs)

[Gateway API](http://127.0.0.1:8484/docs)

## Consumer Applicaiton
[Consumer App UI](http://127.0.0.1:5000)