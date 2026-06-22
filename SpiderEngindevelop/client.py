import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from loguru import logger
from config.settings import settings
from exceptions import RequestException,TimeoutException
from typing import Optional

class CrawlerClient:
    '''封装的HTTP客户端'''

    def __init__(self):
        # 弱私密性
        self._client:Optional[httpx.AsyncClient] = None

    #　异步上下文管理器
    async def __aenter__(self):
        await self.start()
        return self
    async def __aexit__(self,exc_type,exc_val,exc_tb):
        await self.close()

    async def start(self):
        '''启动客户端'''
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=settings.request_timeout,
                follow_redirects=True,
                headers={
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
                }
            )
            logger.debug("HTTP客户端已启动")
    async def close(self):
        '''关闭客户端'''
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP客户端已关闭")

    # 重试策略
    @retry(
        stop=stop_after_attempt(settings.max_retries), #最大次数
        wait=wait_exponential(multiplier=1,max=10), # 指数回避
        retry=retry_if_exception_type((httpx.TimeoutException,httpx.ConnectError)) # 指定异常才重试
    )

    # 发送get请求
    async def get(self,url:str,**kwargs) -> httpx.Response:
        if self._client is None:
            await self.start()

        logger.debug(f"GET请求：{url}")
        try:
            response = await self._client.get(url,**kwargs)
            # 检查http请求
            response.raise_for_status()
            logger.info(f"请求成功：{url}[{response.status_code}]")
            return response

        except httpx.TimeoutException as e:
            logger.warning(f"请求超时{url}")
            raise TimeoutException(f"请求超时：{url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP错误：{url}[{e.response.status_code}]")
            raise RequestException(
                f"HTTP状态码异常：{e.response.status_code}",
                url = url
            ) from e
        except Exception as e:
            logger.exception(f"请求异常：{url}")
            raise RequestException(f"请求异常：{e}",url = url ) from e




