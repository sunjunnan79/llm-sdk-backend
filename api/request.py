from pydantic import BaseModel


class RegisterReq(BaseModel):
    owner: str
    token: str


class SavePromptReq(BaseModel):
    name: str
    prompt: str


class FindPromptReq(BaseModel):
    name: str
