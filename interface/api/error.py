from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, code: int, message: str, data: any = None):
        super().__init__(status_code=400, detail={"code": code, "message": message, "data": data})


# PROMPT
PROMPT_NOT_FIND = CustomException(40001, "不存在的Prompt")

# TOKEN
TOKEN_NOT_FOUND = CustomException(40101, "缺少token")
TOKEN_BAD = CustomException(40102, "错误的token")
TOKEN_BAD_CREATE_TOKEN = CustomException(40103, "错误的注册秘钥")

# SYSTEM
SYSTEM_ERR = CustomException(50001, "系统内部错误")
