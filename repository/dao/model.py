from typing import Optional, Type, Dict

from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = Engine

# 基类
Base = declarative_base()


def InitDB(config: Dict):
    global engine
    mysql_config = config["MYSQL"]

    # 创建所有表
    engine = create_engine(
        url=f"mysql+pymysql://{mysql_config['URL']}",
        echo=True,  # 开启 SQL 日志输出
        pool_size=mysql_config["POOL_SIZE"],  # 设置连接池大小
        max_overflow=20,  # 允许的最大溢出连接数
        pool_recycle=1800,  # 连接空闲超过 1800 秒后自动回收
        pool_pre_ping=True,  # 检查连接是否可用
    )

    Base.metadata.create_all(engine)


class BaseDAO:
    def __init__(self):
        # 设置session
        self.session = sessionmaker(bind=engine)()

    def save(self, obj: Base):
        try:
            # merge 会检查主键是否存在，存在则更新，不存在则插入
            obj = self.session.merge(obj)
            self.session.commit()
            self.session.refresh(obj)  # 确保返回的是最新状态
            return obj
        except Exception as e:
            self.session.rollback()
            raise ValueError("保存失败") from e
        finally:
            self.session.close()

    def delete(self, obj: Base):
        self.session.delete(obj)
        self.session.commit()


# prompt表
class Prompt(Base):
    __tablename__ = "prompt"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    prompt = Column(String(2048), nullable=False)

    # 定义联合唯一约束
    __table_args__ = (
        UniqueConstraint('owner', 'name', name='uq_owner_name'),
    )


class PromptDAO(BaseDAO):
    def find(self, name: str, owner: str) -> Optional[Type[Prompt]]:
        return self.session.query(Prompt).filter_by(name=name, owner=owner).first()

    def findall(self, owner: str) -> list[Type[Prompt]]:
        # 使用 all() 来获取所有数据
        return self.session.query(Prompt).filter_by(owner=owner).all()

    def save(self, prompt: Prompt):
        resp = self.find(prompt.name, prompt.owner)
        if resp is None:
            resp = prompt
        else:
            resp.prompt = prompt.prompt
        BaseDAO.save(self, resp)
