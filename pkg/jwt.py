import datetime
from typing import Dict

import jwt

SECRET_KEY: str
CHECK_TOKEN: str


def initJWT(config: Dict):
    global SECRET_KEY
    SECRET_KEY = config["SECRET_KEY"]
    global CHECK_TOKEN
    CHECK_TOKEN = config["CHECK_TOKEN"]


class JWT(object):

    def issue_license(self, owner: str, features: list = None, duration_days: int = None):
        issued_at = datetime.datetime.utcnow()

        if duration_days is None:
            expires_at = "never"  # 永不过期标志
        else:
            expires_at = (issued_at + datetime.timedelta(days=duration_days)).isoformat()

        payload = {
            "owner": owner,
            "issued_at": issued_at.isoformat(),
            "expires_at": expires_at,
            "features": features
        }

        # 使用私钥生成签名
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def verify_license(self, token: str):
        try:
            # 解码许可证并验证签名
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # 检查过期时间
            expires_at = payload["expires_at"]
            if expires_at != "never":
                expires_at = datetime.datetime.fromisoformat(expires_at)
                if datetime.datetime.utcnow() > expires_at:
                    return False, "License expired"

            return True, payload
        except jwt.ExpiredSignatureError:
            return False, "Signature expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"

    def check_create_token(self, token: str) -> bool:
        return token == CHECK_TOKEN


def getJWT():
    return JWT()
