# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

import time, re, os
import aiohttp, asyncio
from bs4 import BeautifulSoup

'''
第一步，下载出所有车型的网页。
'''


class GetAllHtml(object):
    def __init__(self):
        self.list2 = []  # 接收参数配置页url其中的id

    async def fetch(self, session, url):
        # 获取网页
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        try:
            async with session.get(url, headers=headers, verify_ssl=False) as resp:
                # encoding = resp.get_encoding()
                print(url, resp.status)
                return await resp.text(errors='ignore')
                # return await resp.text(encoding='GB18030')
        except Exception as e:
            print("Connect Error: ", url)
            print("Exception: ", e)

    async def getUrls(self, html):
        # 提取url
        # global list2
        bs = BeautifulSoup(html, "lxml")
        bss = bs.find_all("li")
        for b in bss:
            d = b.h4
            if d:
                her = str(d.a.attrs['href'])
                her = her.split("#")[0]
                her = her[her.index(".cn") + 3:].replace("/", '')
                if her:
                    self.list2.append(her)

    async def downLoad(self, url):
        # 处理网页
        connector = aiohttp.TCPConnector(limit=60)  # urls太多报错ValueError，设置并发数为60
        async with aiohttp.ClientSession(connector=connector) as session:
            html = await self.fetch(session, url)
            await self.getUrls(html)

    async def downHtml(self, url):
        # 下载参数配置页html
        # connector = aiohttp.TCPConnector(limit=64) #urls太多报错ValueError，设置并发数为60
        async with aiohttp.ClientSession() as session:
            print(url)
            id = re.search(r"/(\d+).", url).groups(1)
            html = await self.fetch(session, url)
            if html:
                print("html lenth ", len(html))
            await self.saveHtml(html, id[0])

    async def saveHtml(self, html, id):
        # 在本地保存html
        path = r"./data/html/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + str(id) + ".html", "w", encoding="utf-8") as f:
            f.write(html)

    def main(self):
        # url1列表
        list1 = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        # https://www.autohome.com.cn/grade/carhtml/L.html
        site1 = "https://www.autohome.com.cn/grade/carhtml/"
        urls1 = [site1 + a + ".html" for a in list1]
        # 利用asyncio模块进行异步IO处理：提取 参数配置页url，返回sedUrls
        loop = asyncio.get_event_loop()
        tasks1 = [asyncio.ensure_future(self.downLoad(url)) for url in urls1]
        tasks1 = asyncio.gather(*tasks1)
        loop.run_until_complete(tasks1)
        # https://car.autohome.com.cn/config/series/255.html
        print(len(self.list2), self.list2)
        site2 = "https://car.autohome.com.cn/config/series/"
        urls2 = [site2 + i + ".html" for i in self.list2]
        # 提取html保存至本地
        for url in urls2:
            coroutine = self.downHtml(url)
            task = asyncio.ensure_future(coroutine)
            loop.run_until_complete(task)


if __name__ == '__main__':
    start = time.time()
    GetAllHtml().main()
    print("耗时： ", time.time() - start)
