from typing import TypeVar, Generic, List

from pydantic import BaseModel


class RegisterResp(BaseModel):
    token: str


# 保存Prompt的返回结构
class SavePromptResp(BaseModel):
    name: str
    prompt: str


class FindPromptResp(BaseModel):
    name: str
    prompt: str


class FindAllPromptResp(BaseModel):
    prompts: List[FindPromptResp]


# 定义类型变量 T，表示 data 字段的类型
T = TypeVar('T')


class Resp(BaseModel, Generic[T]):
    msg: str = ""
    code: int = 0
    data: T  # 使用类型变量 T 来指定 data 字段的类型,实现了动态类型返回
