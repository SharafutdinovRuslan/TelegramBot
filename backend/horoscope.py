import requests
from bs4 import BeautifulSoup


def get_today_horoscope(znak: str):
    response = requests.get(
        url="https://1001goroskop.ru/",
        params={
            "znak": znak.strip().lower(),
        },
    )

    soup = BeautifulSoup(response.text, features="lxml").find("table")
    forecast = next(soup.stripped_strings)
    return forecast
