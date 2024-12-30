import uvicorn

from config import config
from pkg import jwt
from repository.dao import model
from router.handlers import app


def init():
    try:
        conf = config.initConfig('config/config.yaml')
        model.InitDB(conf)
        jwt.initJWT(conf)
    except Exception as e:
        exit(e)


if __name__ == "__main__":
    init()
    uvicorn.run(app, host="0.0.0.0", port=5000)
