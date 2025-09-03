import aiohttp
from bs4 import BeautifulSoup



async def translate(text: str, language_to: str, language_from: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://translate.google.com/m?tl={language_to}&sl={language_from}&q={text}') as \
            response:
            result = await response.text()
            source = BeautifulSoup(result, "lxml")

            return source.find("div", attrs={"class": "result-container"}).text

