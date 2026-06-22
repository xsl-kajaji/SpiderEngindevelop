import asyncio
import os

from loguru import logger

from learn_pandas.SpiderEngindevelop.exceptions import CrawlerException
from logger_config import setup_logger
from crawler import MingJuCrawler
from config.settings import settings
import ujson

async def main():
    # 初始化日志
    setup_logger()

    logger.info(f"爬虫运行环境环境:{settings.env}")
    logger.info(f"调试模式：{settings.debug}")
    logger.info(f"目标页数：{settings.first_n_page}")

    # 创建输出目录
    os.makedirs(settings.output_dir, exist_ok=True)

    # 创建爬虫实例
    crawler = MingJuCrawler()

    try:
        # 运行爬虫
        result = await crawler.run()

        # 保存结果
        output_file = f"{settings.output_dir}/crawler_result.json"
        with open(output_file,"w",encoding="utf-8") as f:
            ujson.dump(result.model_dump(),f,ensure_ascii=False,indent=2)

        logger.info(f"结果已保存到：{output_file}")

    except CrawlerException as e:
        logger.error(f"爬虫异常：{e}")
        raise

    except Exception as e:
        logger.exception(f"未预期的异常：{e}")
        raise

    finally:
        await crawler.cleanup()
        logger.info("爬虫运行结束")


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.critical(f"程序异常退出:{e}")

if __name__ == "__main__":
    run()