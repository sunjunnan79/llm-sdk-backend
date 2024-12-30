import json
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from interface.api import CustomException, TOKEN_NOT_FOUND, TOKEN_BAD
from interface.router.prompt import promptRouter
from interface.router.token import tokenRouter
from pkg.jwt import getJWT

# 初始化app
app = FastAPI(
    title="API 文档标题",
    description="接口的详细描述",
    version="1.0.0"
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


# jwt验证中间件
class CustomMiddleware(BaseHTTPMiddleware):
    jwt = getJWT()

    async def dispatch(self, request: Request, call_next: Callable):
        # 这个地方非常愚蠢的做法,但是fastapi不允许分组应用中间件所以只能这么做了
        if not request.url.path.startswith("/token"):
            # 获取请求头中的信息，比如 Authorization 或其他自定义头
            login_token = request.headers.get("Authorization")  # 假设登录令牌在 Authorization 头中

            if login_token:
                ok, payload = self.jwt.verify_license(login_token)
                if ok and payload.get("owner"):
                    request.state.owner = payload.get("owner")
                else:
                    raise TOKEN_BAD
            else:
                raise TOKEN_NOT_FOUND

        # 调用下一个请求处理函数
        response = await call_next(request)
        return response


# 创建需要验证的路由组
app.include_router(promptRouter)
app.include_router(tokenRouter)

app.add_middleware(CustomMiddleware)


# 配置全自动捕获错误
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    # 打印错误日志
    print(f"Error: {exc.detail} from {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


# 导出 OpenAPI JSON 文件
@app.on_event("startup")
async def export_openapi():
    openapi_data = app.openapi()  # 获取 OpenAPI JSON 数据
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, ensure_ascii=False, indent=4)
    print("OpenAPI 文档已导出为 openapi.json")
