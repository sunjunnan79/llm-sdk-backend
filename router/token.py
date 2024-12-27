from fastapi import Depends, APIRouter

from api import request, response
from api.response import RegisterResp, Resp
from service.token import TokenService

tokenRouter = APIRouter()


def get_service() -> TokenService:
    return TokenService()


@tokenRouter.post("/token/register", tags=["token"], response_model=Resp[RegisterResp], summary="注册",
                  description="寻找提示词")
async def Register(req: request.RegisterReq, service: TokenService = Depends(get_service)):
    return response.Resp(msg="注册成功!", data=service.Register(req))