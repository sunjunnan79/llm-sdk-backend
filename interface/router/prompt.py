from fastapi import Depends, Request, APIRouter

from interface.api import Resp, SavePromptResp, FindPromptResp
from interface.api import response, request
from service.prompt import PromptService

promptRouter = APIRouter()


def get_service() -> PromptService:
    return PromptService()


# 控制器函数，可以在这里进行登录信息的验证等操作
def get_owner(request: Request):
    return request.state.owner  # 这里获取到登录令牌


@promptRouter.put("/prompt/save", tags=["prompt"], response_model=Resp[SavePromptResp], summary="保存提示词",
                  description="保存提示词,如果已经存在会覆盖原来的")
async def SavePrompt(
        req: request.SavePromptReq,
        service: PromptService = Depends(get_service),
        owner: str = Depends(get_owner)
):
    """
        保存提示词接口

        保存用户的提示词。如果提示词已经存在，则会覆盖原来的内容。

        Args:
            req (request.SavePromptReq): 提交的保存提示词请求

        Returns:
            Resp: 包含保存结果的响应数据，返回保存的提示词信息。

        - **成功**: 返回保存成功的提示词信息。
        - **失败**: 返回错误信息，提示词保存失败。

        Summary:
            保存提示词，如果已存在则覆盖。

        Description:
            该接口用于保存一个提示词，如果同名的提示词已经存在，会直接覆盖原有提示词的内容。
        """

    return response.Resp(msg="保存提示词成功", data=service.SavePrompt(owner, req))


@promptRouter.post("/prompt/find", tags=["prompt"], response_model=Resp[FindPromptResp], summary="查找提示词",
                   description="寻找提示词")
async def FindPrompt(
        req: request.FindPromptReq,
        service: PromptService = Depends(get_service),
        owner: str = Depends(get_owner)
):
    """
           查询提示词接口

           保存用户的提示词。如果提示词已经存在，则会覆盖原来的内容。

           Args:
               req (request.SavePromptReq): 提交的保存提示词请求

           Returns:
               Resp: 包含保存结果的响应数据，返回保存的提示词信息。

           - **成功**: 返回保存成功的提示词信息。
           - **失败**: 返回错误信息，提示词保存失败。

           Summary:
               保存提示词，如果已存在则覆盖。

           Description:
               该接口用于保存一个提示词，如果同名的提示词已经存在，会直接覆盖原有提示词的内容。
           """
    return response.Resp(msg="获取prompt成功", data=service.FindPrompt(owner, req))
