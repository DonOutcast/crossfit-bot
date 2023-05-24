from bs4 import BeautifulSoup
from aiohttp import ClientSession
from datetime import datetime


async def fetch_xml(session: ClientSession) -> BeautifulSoup:
    url = "http://www.cbr.ru/scripts/XML_daily.asp?"
    today = datetime.today()
    today = today.strftime("%d/%m/%Y")
    url += "date_req?=" + str(today)
    async with session.get(url) as response:
        xml_content = await response.text()
        soup = BeautifulSoup(xml_content, features='lxml')
        return soup


async def fetch_one_currency(session: ClientSession, id_currency) -> BeautifulSoup:
    url = "http://www.cbr.ru/scripts/XML_daily.asp?"
    today = datetime.today()
    today = today.strftime("%d/%m/%Y")
    url += "date_req?=" + str(today)
    async with session.get(url) as response:
        xml_content = await response.text()
        soup = BeautifulSoup(xml_content, features='lxml')
    return soup.find("valute", {"id": id_currency})
