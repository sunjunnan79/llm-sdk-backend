from api import request, response, error
from model.model import PromptDAO, Prompt


class PromptService:
    def __init__(self):
        self.PromptDAO = PromptDAO()

    def FindPrompt(self, owner: str, req: request.FindPromptReq) -> response.FindPromptResp:

        prompt = self.PromptDAO.find(req.name, owner)
        if prompt:
            return response.FindPromptResp(name=req.name, prompt=prompt.prompt)
        else:
            raise error.PROMPT_NOT_FIND

    def FindAllPrompt(self, owner: str) -> response.FindAllPromptResp:

        prompts = self.PromptDAO.findall(owner)
        if prompts:

            # 定义返回结果
            resp = response.FindAllPromptResp()

            # 类型转换
            for prompt in prompts:
                resp.prompts.append(response.FindAllPromptResp(
                    name=prompt.name,
                    prompt=prompt.prompt)
                )

            return resp
        else:
            raise error.PROMPT_NOT_FIND

    def SavePrompt(self, owner: str, req: request.SavePromptReq) -> response.SavePromptResp:
        try:
            self.PromptDAO.save(Prompt(
                owner=owner,
                name=req.name,
                prompt=req.prompt
            )
            )
            return response.SavePromptResp(
                name=req.name,
                prompt=req.prompt
            )
        except:
            raise error.SYSTEM_ERR
