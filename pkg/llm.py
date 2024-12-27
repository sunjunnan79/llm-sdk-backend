# 分割工具
import re

import tiktoken
from langchain.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# RAG工具

#


# 初始化模型,如果要添加的话请在这里进行添加

def initModels(config):
    models = {}

    models["gpt-4o"] = ChatOpenAI(model="gpt-4o", openai_api_key=config.api_key,
                                  base_url=config.base_url) | StrOutputParser()

    models["gpt-3.5"] = ChatOpenAI(model="gpt-3.5", openai_api_key=config.api_key,
                                   base_url=config.base_url) | StrOutputParser()

    models["llama3.2"] = Ollama(model="llama3.2") | StrOutputParser()

    return models


def split_text_by_token_limit(prompt: str, max_tokens: int = 3500, model: str = "gpt-4o"):
    """
    按 Token 限制对文本进行语义分割
    :param prompt: 输入的文本
    :param max_tokens: 每段的最大 Token 数
    :param model: 使用的 GPT 模型（如 gpt-4o）
    :return: 切分后的文本段落列表
    """

    # 加载模型对应的编码器
    encoding = tiktoken.encoding_for_model(model)

    # 按句子切分文本（通过句号、问号、感叹号分割）
    sentences = re.split(r'(?<=[。！？\?])', prompt)

    chunks = []  # 存储切分后的段落
    current_chunk = []  # 当前段落
    current_tokens = 0  # 当前段落的 Token 数量

    for sentence in sentences:
        if not sentence.strip():  # 跳过空句子
            continue

        sentence_tokens = len(encoding.encode(sentence))

        # 如果当前段落加上新句子会超出 Token 限制，则保存当前段落
        if current_tokens + sentence_tokens > max_tokens:
            chunks.append("".join(current_chunk))
            current_chunk = []
            current_tokens = 0

        # 添加句子到当前段落
        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    # 保存最后的段落
    if current_chunk:
        chunks.append("".join(current_chunk))

    return chunks
