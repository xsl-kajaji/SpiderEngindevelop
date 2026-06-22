from typing import Optional


class CrawlerException(Exception):
    # 爬虫基础异常

    def __init__(self,message:str,url:Optional[str] = None):
        self.message = message
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        if self.url:
            return f"{self.message}(URL:{self.url})"
        return self.message

class RequestException(CrawlerException):
    # 请求相关异常
    pass

class ParseException(CrawlerException):
    # 解析相关异常
    pass

class StorageException(CrawlerException):
    # 存储相关异常
    pass

class RateLimitException(CrawlerException):
    # 触发速率限制
    pass

class IPBlockException(RequestException):
    # IP被封禁
    pass

class PageNotFoundException(RequestException):
    # 页面不存在
    pass

class TimeoutException(RequestException):
    # 请求超时
    pass

class HTTPStatusException(RequestException):
    # http 状态码异常
    def __init__(self,message:str,status_code:int,url:Optional[str]=None):
        self.status_code = status_code
        super().__init__(message,url)