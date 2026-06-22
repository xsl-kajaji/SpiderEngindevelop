import asyncio
from typing import List

from client import CrawlerClient

from model import MingJu,MingJuResult
from parser import MingJuParser
from loguru import logger
from config.settings import settings
from exceptions import CrawlerException

class MingJuCrawler:
    '''名句爬虫'''
    def __init__(self):
        self.client = CrawlerClient()
        self.parser = MingJuParser()
        self.result = MingJuResult()

    async def run(self) :
        """运行爬虫"""
        logger.info(f"开始爬取任务-目标：前{settings.first_n_page}页")
        async with self.client:
            previous_number = await self._get_previous_page_number()
            await self._crawler_item_list(previous_number)

        return self.result

    async def _get_previous_page_number(self):
        '''获取下一页分页号'''
        logger.info(f"获取分页信息。。。")

        url = f"{settings.base_host}/mingjus/"
        response = await self.client.get(url)
        page_number = self.parser.parse_previous_page(response.text)

        logger.info(f"当前页码：{page_number - 1}")
        return page_number

    async def _crawler_item_list(self,previous_number:int)-> List[MingJu]:
        '''爬取帖子列表'''
        logger.info(f"开始爬取名句列表")

        all_items: List[MingJu] = []
        start_page = previous_number - 1
        end_page = settings.first_n_page - start_page
        for page_num in range(start_page, end_page,1):
            try:
                url = f"{settings.base_host}/mingjus/default.aspx?page={page_num}&tstr=&astr=&cstr=&xstr="
                logger.info(f"爬取第{page_num}页")

                response = await self.client.get(url)
                items = self.parser.parse_note_list(response.text)
                all_items.extend(items)

                logger.info(f"第{page_num}页获取{len(items)}个名句")

                # 请求间隔
                await asyncio.sleep(settings.request_delay)
            except CrawlerException as e:
                logger.warning(f"第{page_num}页爬取失败：{e}")

        logger.info(f"名句爬取完成，共{len(all_items)}个帖子")

        self.result.item.extend(all_items)

        return all_items


    async def cleanup(self):
        '''清理资源'''
        logger.debug(f"执行清理")
        await self.client.close()






