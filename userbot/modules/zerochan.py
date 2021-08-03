import json
import logging

import scrapy
from scrapy.crawler import CrawlerProcess
from telethon.errors import MediaEmptyError, WebpageCurlFailedError
from telethon.events import NewMessage

from .. import LOGS
from .. import app as client
from ..events import newMessage

# logging.getLogger('scrapy').propagate = False  # deshabilitar del todo
logging.getLogger('scrapy').setLevel(logging.WARNING)

items = []


# SPIDER
class WeekPopularSpider(scrapy.Spider):
    name = 'week_popular'
    allowed_domains = ['www.zerochan.net/']
    start_urls = ['http://www.zerochan.net/?s=fav&t=1&d=1']

    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    #     "FEEDS": {
    #         "items.json": {
    #             "format": "json"
    #         },
    #     },
    #     'LOG_ENABLED': False
    # }

    def parse(self, response):
        global items
        item = []
        data = json.loads(
            response.xpath(
                '//*[@id="content"]/script//text()').extract_first())
        for image in data['itemListElement']:
            item.append({"name": image['name'], "url": image['url']})
            items.extend(item)
            yield item


def crawl():
    process = CrawlerProcess()
    process.crawl(WeekPopularSpider)
    process.start()


# noinspection SpellCheckingInspection
@newMessage(pattern='zerochan')
async def _(event: NewMessage.Event):
    global items
    await event.edit('Procesando...\nEspere, puede demorar')

    crawl()

    media = []
    for image in items:

        try:
            img = await client.send_file('me',
                                         file=image['url'],
                                         caption=image['name'],
                                         silent=True)

        except MediaEmptyError:
            LOGS.exception(f"MEDIAEMPTY: {image['name']} {image['url']}",
                           exc_info=False)
            continue
        except WebpageCurlFailedError:
            LOGS.exception(f"WEBCURL: {image['name']} {image['url']}")
            continue
        except:
            LOGS.exception(f"NO CONOCIDO: {image['name']} {image['url']}")
            continue

        media.append(img)
    items = []
    await client.send_file(event.chat_id,
                           file=[photo.media for photo in media],
                           caption=[caption.message for caption in media])
    await event.client.delete_messages('me', [m.id for m in media])
    return await event.delete()
