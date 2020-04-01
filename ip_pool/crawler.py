# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
from ip_pool.utils import get_page
from pyquery import PyQuery as pq
from lxml import etree
import requests
import re


class ProxyMetaclass(type):
    """获取代理类的类，即Crawler的元类"""
    def __new__(cls, name, bases, attrs):
        count, nums = 0, 0
        attrs["__CrawlFunc__"] = []
        attrs["__MoneyFunc__"] = []
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
            elif "money_" in k:
                attrs["__MoneyFunc__"].append(k)
                nums += 1
        attrs["__CrawlFuncCount__"] = count
        attrs["__MoneyFuncCount__"] = nums
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """获取代理类"""
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理", proxy)
            proxies.append(proxy)
        return proxies

    # 网站已更新，待研究
    def crawl_daili66(self, page_count=4):
        """
        抓取代理66 此网站ip代理丰富 提供了大量的国外ip代理
        :param page_count:页码
        :return: 抓取的代理
        """
        start_url = "http://www.66ip.cn/{}.html"  # 此链接提供了大量的国内外免费的ip代理，页码数1931，代理总数：3724
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc(".containerbox table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ":".join([ip, port])

    def crawl_daili66free(self, num=100):
        """
        提取代理66提供的没费ip代理接口
        :param num: 默认一次提取100个
        :return:
        """
        start_url = "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=4&start=&ports=&export=&" \
                    "ipaddress=&area=1&proxytype=2&api=66ip".format(num)
        response = requests.get(
            url=start_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/80.0.3987.132 Safari/537.36",
            }
        ).content.decode("gbk")
        pattern = re.compile(r'\d+\.\d+\.\d+\.\d+\:\d+', re.S)
        ip_port_li = pattern.findall(response)
        for ip_port in ip_port_li:
            yield ip_port

    def crawl_89ip(self, num=100):
        """
         提取89免费代理
        :param num: 默认一次提取100个
        :return:
        """
        start_url = "http://www.89ip.cn/tqdl.html?num={}&address=&kill_address=&port=&kill_port=&isp=".format(num)
        html = get_page(start_url)
        response = etree.HTML(html)
        ip_port_li = response.xpath('//div[@style="padding-left:20px;"]/text()')[:-1]
        for ip_port in ip_port_li:
            yield ip_port.strip()

    def crawl_ip366(self):
        """
        抓取云代理
        :return:抓取的代理
        """
        for page in range(1, 4):  # 目前本网站已更新到7页免费代理
            start_url = "http://www.ip3366.net/free/?stype=1&page={}".format(page)
            html = get_page(start_url)
            response = etree.HTML(html)
            trs = response.xpath("//div[@id='list']/table//tr")[1:]
            for tr in trs:
                ip = tr.xpath("./td[1]/text()")[0].strip()
                port = tr.xpath("./td[2]/text()")[0].strip()
                yield ":".join([ip, port])

    def crawl_kuaidaili(self):
        """
        抓取快代理
        :return:抓取的代理
        """
        for i in range(1, 4):  # 本网站免费代理较多，页码数为3362
            start_url = "https://www.kuaidaili.com/free/inha/{}/".format(i)
            html = get_page(start_url)
            if html:
                ip_pattern = re.compile(r'<td data-title="IP">(.*?)</td>')
                ip = ip_pattern.findall(html)
                port_pattern = re.compile(r'<td data-title="PORT">(.*?)</td>')
                port = port_pattern.findall(html)
                for ip, port in zip(ip, port):
                    ip_port = ip+":"+port
                    yield ip_port.replace(" ", "")

    def crawl_xicidaili(self):
        """
        抓取西祠免费代理
        :return: 抓取到的代理
        """
        for i in range(1, 3):  # 本网站免费代理较多，页码为4052
            start_url = "https://www.xicidaili.com/nn/{}".format(i)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                          "application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "Connection": "keep-alive",
                "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTYzNGYxMDI0ZTQyYTFiY2M3NmU5MjhkZGM5Yzd"
                          "kNDhlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWo3aVVEbER4dGpLSFdzTEdGNERTbGQ5OGQ0ekoxWDFwUm9kUkMrcG5"
                          "ReDQ9BjsARg%3D%3D--1c2745a54b00042c950d46dbb785f4bab0756adb; Hm_lvt_0cf76c77469e965d2957f05"
                          "53e6ecf59=1585454330; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1585454780",
                "Host": "www.xicidaili.com",
                "If-None-Match": "W/be944a45da779bcfb93e7d26e93e91a6",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/80.0.3987.132 Safari/537.36",
            }
            html = get_page(start_url, options=headers)
            if html:
                trs_pattern = re.compile(r'<tr class=.*?>(.*?)</tr>', re.S)
                trs = trs_pattern.findall(html)
                for tr in trs:
                    ip_pattren = re.compile(r'\d+\.\d+\.\d+\.\d+')
                    ip_address = ip_pattren.findall(tr)
                    port_pattern = re.compile(r'<td>(\d+)</td>')
                    port = port_pattern.findall(tr)
                    for address, port in zip(ip_address, port):
                        ip_port = address+":"+port
                        yield ip_port.replace(" ", "")

    def money_xdl(self):
        """
        讯代理提取
        :return:
        """
        api = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=31fe894efe894d7a95b285e3ea2ac530&orderno=YZ20203304582Q3oXs2&returnType=2&count=20"
        json_str = requests.get(url=api).json()
        ip_port_li = json_str.get("RESULT")
        for ip_port in ip_port_li:
            ip = ip_port.get("ip")
            port = ip_port.get("port")
            yield ip+":"+port



