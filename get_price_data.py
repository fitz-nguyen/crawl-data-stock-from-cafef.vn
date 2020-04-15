import requests
import asyncio
from time import time
import json
import concurrent.futures
from bs4 import BeautifulSoup
import pandas as pd
import asyncio

loop = asyncio.get_event_loop()
list_code = pd.read_excel("code_stock.xlxs")


def get_data(code="VIC", page=1):
    print("code, page", code, page)
    df = pd.DataFrame(columns=["code", "date", "modificable_price", "close_price", "change_price_value", "change_price_percent", "open_price", "KL_GD_khoplenh", "GT_GD_khoplenh",
                               "KL_GD_thoathuan", "GT_GD_thoathuan", "highest_price", "lowest_price"])
    URL = f"https://s.cafef.vn/Lich-su-giao-dich-{code}-1.chn"
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
        "Cookie": "_ga=GA1.2.1063637455.1585215340; favorite_stocks_state=1; _uidcms=1585215340247638741; _gid=GA1.2.1677237587.1586756506; \
        cafef.IsMobile=IsMobile=NO; ASP.NET_SessionId=wqjhet2gh2fwaqr11xugxear; _ga=GA1.3.1063637455.1585215340; _gid=GA1.3.1677237587.1586756506",
    }

    body = f"ctl00%24ContentPlaceHolder1%24scriptmanager=ctl00%24ContentPlaceHolder1%24ctl03%24panelAjax%7Cctl00%24ContentPlaceHolder1%24ctl03%24pager2&ctl00%24ContentPlaceHolder1%24ctl03%24txtKeyword={code}&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate1%24txtDatePicker=&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate2%24txtDatePicker=&ctl00%24UcFooter2%24hdIP=&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24ctl03%24pager2&__EVENTARGUMENT={page}&__VIEWSTATE=%2FwEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY3RsMDMkYnRTZWFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ%3D%3D&__VIEWSTATEGENERATOR=2E2252AF&__ASYNCPOST=true&"

    resps = requests.post(URL, headers=hdr, data=body)
    soup = BeautifulSoup(resps.content, 'html.parser')
    table = soup.find('table', id='GirdTable2').find_all('tr')[2:]

    def _str_to_float(string):
        string = string.encode(
            'utf-8').decode(
                'utf-8').replace(
                    '\xa0', '').replace(
                        ',', '').replace(
                            "(", "").replace(" %)", "")

        return float(string)

    for row in table:
        columns = row.find_all('td')

        change_price_value, _, change_price_percent = columns[3].get_text().partition(" ")
        df = df.append({
            "code": code,
            "date": columns[0].get_text(),
            "modificable_price": _str_to_float(columns[1].get_text()),
            "close_price": _str_to_float(columns[2].get_text()),
            "change_price_value": _str_to_float(change_price_value),
            "change_price_percent": _str_to_float(change_price_percent),
            "KL_GD_khoplenh": _str_to_float(columns[5].get_text()),
            "GT_GD_khoplenh": _str_to_float(columns[6].get_text()),
            "KL_GD_thoathuan": _str_to_float(columns[7].get_text()),
            "GT_GD_thoathuan": _str_to_float(columns[8].get_text()),
            "open_price": _str_to_float(columns[9].get_text()),
            "highest_price": _str_to_float(columns[10].get_text()),
            "lowest_price": _str_to_float(columns[11].get_text())
        }, ignore_index=True)

    return df


def get_all_data(code="VIC"):
    available = True
    try:
        df = pd.read_csv(f'data-all/{code}.csv')
    except Exception as e:
        df = pd.DataFrame(columns=["code", "date", "modificable_price", "close_price", "change_price_value", "change_price_percent", "open_price", "KL_GD_khoplenh", "GT_GD_khoplenh",
                                   "KL_GD_thoathuan", "GT_GD_thoathuan", "highest_price", "lowest_price"])

    for i in (range(1, 300)):
        df_resp = get_data(page=i, code=code)
        if df_resp.empty or available is False:
            break
        df = pd.concat([
            df, df_resp
        ], ignore_index=True).reset_index(drop=True)

    df = df.drop_duplicates(subset="date")
    df.to_csv(f'{code}.csv', index=False)


if __name__ == "__main__":
    # codes = list_code[(list_code["Unnamed: 2"] == "HSX") & (
    #     list_code["Unnamed: 0"].str.len() == 3)]["Unnamed: 0"].tolist()
    codes = list_code[(list_code["Unnamed: 0"].str.len() == 3)]["Unnamed: 0"].tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=600) as executor:
        executor.map(get_all_data, codes)
