from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class CrawlerSettings(BaseSettings):
    '''爬虫配置'''
    # 基础配置
    env:str = Field(default="development",description="运行环境")
    debug:bool = Field(default=True,description="调试模式")
    log_level:str = Field(default="DEBUG",description="日志级别")

    # 请求配置
    first_n_page:int = Field(default=6,description="爬取前N页")
    base_host:str = Field(default="https://www.guwendao.net",description="目标站点")
    request_timeout:int = Field(default=30,description="请求超时时间")
    request_delay:float = Field(default=0.5,description="请求间隔")
    max_retries:int = Field(default=3,description="最大重试次数")
    retry_delay:float = Field(default=1.0,description="重试延迟（秒）")

    #　并发配置
    max_concurrent:int = Field(default=10,description="最大并发数")

    # 数据库配置
    db_host:str = Field(default="localhost",description="数据库主机")
    db_port:int = Field(default=3306,description="数据库端口")
    db_user:str = Field(default="root",description="数据库用户")
    db_password:str = Field(default="",description="数据库密码")
    db_name:str = Field(default="",description="数据库名")

    # 输出配置
    output_dir:str = Field(default="./output",description="输出目录")
    log_dir:str = Field(default="./logs",description="日志目录")

    # 代理配置
    proxy_url:Optional[str] = Field(default=None,description="代理地址")

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
        #　环境变量前缀，如CRAWLER_DEBUG=true
        env_prefix = "CRAWLER_"

# 全局配置实例
settings = CrawlerSettings()