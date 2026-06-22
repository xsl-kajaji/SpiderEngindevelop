from parsel import Selector
from loguru import logger
from typing import List,Optional

from learn_pandas.SpiderEngindevelop.exceptions import ParseException
from learn_pandas.SpiderEngindevelop.model import MingJu


class MingJuParser:
    '''页面解析器'''

    @staticmethod
    def parse_previous_page(html:str) -> int:
        '''解析获取分页号'''
        try:
            selector = Selector(html)
            page_link = selector.css('a.amore').attrib.get("href","")

            page_number = int(
                page_link
                .replace("/mingjus/default.aspx?page=","")
                .replace("&tstr=&astr=&cstr=&xstr=","")
            )

            logger.debug(f"解析到下一页分页号：{page_number}")

            if not page_link:
               logger.info(f'已到达最大页码：{page_number}页')

            return page_number

        except Exception as e:
            logger.error(f"解析分页号失败：{e}")
            raise ParseException(f"解析分页号失败：{e}")

    @staticmethod
    def parse_note_list(html:str) -> List[MingJu]:
        '''解析获取信息列表'''
        items = []
        selector = Selector(html)

        try:
            contents = selector.css('div.left div.cont')
            for content in contents:
                # 生成数据对象
                item = MingJu()
                item.sentence = content.css('a:nth-of-type(1)::text').get().strip() if content.css(
                    'a:nth-of-type(1)::text') else ''
                item.source = content.css('a:nth-of-type(2)::text').get().strip() if content.css(
                    'a:nth-of-type(2)::text') else ''
                item.href = content.css('a:nth-of-type(1)').attrib.get("href", "").strip() if content.css(
                    'a:nth-of-type(1)::text') else ''

                # 跳过无链接的句子
                if item.href:
                    items.append(item)

        except Exception as e:
            logger.error(f"解析名句列表失败：{e}")
            raise ParseException(f"解析句子列表失败：{e}")

        logger.debug(f"解析到{len(items)}个句子")
        return items
