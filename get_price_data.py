import requests
import asyncio
from time import time
import json
import threading
import concurrent.futures
from bs4 import BeautifulSoup

URL = "https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn"
hdr = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Sec-Fetch-Dest": "empty",
    "X-MicrosoftAjax": "Delta=true",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Origin": "https://s.cafef.vn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Referer": "https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn",
    "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
    "Cookie": "_ga=GA1.2.1063637455.1585215340; favorite_stocks_state=1; _uidcms=1585215340247638741; _gid=GA1.2.1677237587.1586756506; cafef.IsMobile=IsMobile=NO; ASP.NET_SessionId=wqjhet2gh2fwaqr11xugxear; _ga=GA1.3.1063637455.1585215340; _gid=GA1.3.1677237587.1586756506",

}

body = "ctl00%24ContentPlaceHolder1%24scriptmanager=ctl00%24ContentPlaceHolder1%24ctl03%24panelAjax%7Cctl00%24ContentPlaceHolder1%24ctl03%24pager2&ctl00%24ContentPlaceHolder1%24ctl03%24txtKeyword=VNINDEX&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate1%24txtDatePicker=&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate2%24txtDatePicker=&ctl00%24UcFooter2%24hdIP=&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24ctl03%24pager2&__EVENTARGUMENT=1&__VIEWSTATE=%2FwEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY3RsMDMkYnRTZWFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ%3D%3D&__VIEWSTATEGENERATOR=2E2252AF&__ASYNCPOST=true&"


def get_data():
    try:
        resps = requests.post(URL, headers=hdr, data=body)
        soup = BeautifulSoup(resps.content, 'html.parser')
        print(resps.status_code)
        table = soup.find('table', id='GirdTable2').find_all('tr')[2:]
        print(len(table))
        print(table)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # list_index = [i for i in range(1000)]
    # start = time()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=700) as executor:
    #     executor.map(get_data, [1, ])
    # print(time() - start)

    test = get_data()
