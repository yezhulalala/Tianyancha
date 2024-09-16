import requests
import time
from bs4 import BeautifulSoup


def set_proxies(server_ip:str = None,
                server_port:int = None):
    if server_ip is not None and server_port is not None:
        proxies = {
            'http': f'{server_ip}:{server_port}',
            'https': f'{server_ip}:{server_port}',
        }
    else:
        proxies = {}
    return proxies



class TYC():
    def __init__(self, proxies:dict = {}) -> None:
        self.success = True
        self.proxies = proxies

    def new_session(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        session = requests.session()
        res = session.get('https://www.tianyancha.com/', headers=headers, proxies=self.proxies)
        if res.status_code == 200:
            self.CUID = res.cookies.get("CUID")
            self.TYCID = res.cookies.get("TYCID")
            self.success = True
        else:
            self.success = False

    def new_timestamp(self):
        _ = int(time.time()*1000)
        return _

    def search(self, companyName:str)->str:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tianyancha.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.tianyancha.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'X-TYCID': self.TYCID,
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        params = {
            '_': self.new_timestamp(),
        }
        json_data = {
            'keyword': companyName,
        }
        response = requests.post(
            'https://capi.tianyancha.com/cloud-tempest/search/suggest/v5',
            params=params,
            headers=headers,
            json=json_data,
            proxies=self.proxies
        )
        if response.status_code == 200:
            data = response.json().get('data')
            if data:
                for d in data:
                    graphId = d.get('graphId')
                    comName = d.get('comName')
                    if comName == companyName:
                        print(f"Found {comName} as graphId = {graphId}")
                        return graphId
        else:
            self.success = False

    def fetch_basic(self, graphId:str)->dict:
        cookies = {
            'TYCID': self.TYCID,
            'CUID': self.CUID,
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'HWWAFSESID=9a8aa2a7f73bfc81964; HWWAFSESTIME=1726140749912; csrfToken=6G0xc7XZcIJIQH0gwkRhEZ82; TYCID=b4b6aba070fa11efa5a60532fd6ea836; CUID=12cfb735b0cd2df652e50449091f2150; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22191e601ac947a7-0bd1c95bcb772f8-17525637-3686400-191e601ac95232f%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxZTYwMWFjOTQ3YTctMGJkMWM5NWJjYjc3MmY4LTE3NTI1NjM3LTM2ODY0MDAtMTkxZTYwMWFjOTUyMzJmIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22191e601ac947a7-0bd1c95bcb772f8-17525637-3686400-191e601ac95232f%22%7D; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1726140755; HMACCOUNT=7D64C730722A7490; bannerFlag=true; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1726141013',
            'Pragma': 'no-cache',
            'Referer': 'https://www.tianyancha.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        response = requests.get(f'https://www.tianyancha.com/company/{graphId}', cookies=cookies, headers=headers, proxies=self.proxies)

        soup = BeautifulSoup(response.text)
        baseInfo = soup.find("div", attrs={'data-dim': "baseInfo"})

        table = {}
        for tr in baseInfo.find_all("tr"):
            key = None
            value = None
            for idx, td in enumerate(tr.find_all("td")):
                if idx % 2 == 0:
                    key = td.text
                else:
                    value = td.text
                    table.update({
                        key: value
                    })
                    key, value = None, None
        return table
