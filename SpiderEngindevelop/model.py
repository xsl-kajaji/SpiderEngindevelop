from typing import List,Optional
from pydantic import BaseModel,Field

class MingJu(BaseModel):
    """名句列表"""
    sentence:str = Field(default="",description="名句句子")
    source:str = Field(default="",description="名句来源")
    href:str = Field(default="",description="名句链接")

class MingJuResult(BaseModel):
    item:List[MingJu] = Field(default_factory=list,description="名句列表")

