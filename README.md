# Sample Shopping cart
> The stateless shopping cart back-end with python and fastapi framework.

## Getting Started

To get started make sure the following requirements (for development and deployment tooling) are installed on your system:

- [Python 3.9.7+](https://www.python.org/downloads/) (Project Programming Language)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (Python Dependency Manager)
- [Docker](https://hub.docker.com/) (Containerization)
- [Docker Compose](https://docs.docker.com/compose/) (Composer for Docker)

> This project uses [Fake APIs](https://fakestoreapi.com/) to obtain fake sample data to representation of project efficiency. 

To getting started with deployment:

1. You have to implement .env file in the root of project but what is the structure of this file:
    ```
    CART_PATH_PREFIX="/api"
    # Authentication
    SECRET_KEY=secret
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    SERVICE_PORT=5000
    ```
2. run following command to build docker image and start container:
    ```
    docker-compose up -d
    ``` 
### Playing with the Shopping Cart Service
To get endpoints list and playing with endpoints open following link in your browser to see swagger docs:

```
http://localhost:5000/docs
```



### Development
First, make sure that the project dependencies have been installed with the following commands to run uvicorn:

> If you don't have `virtualenv` currently installed, then run `pip install virtualenv`.
```bash
virtualenv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python app/main.py init && \
python app/main.py start
```

## Todo

- Add testing
- Add support for monitoring
- Add better support for logging
- Implement better error handling
- Implement incomplete endpoints

