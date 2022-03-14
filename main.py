from dotenv import load_dotenv
import requests
import os
from urllib.parse import urlparse
import argparse


load_dotenv()

parser = argparse.ArgumentParser(
    description='Создание битлинка и подсчёт кликов по битлинку'
)
parser.add_argument('link', help='Ссылка')
args = parser.parse_args()



def shorten_link(token, url):
    bitlinks_site = "https://api-ssl.bitly.com/v4/bitlinks"
    
    response = requests.post(
        bitlinks_site,
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json= {
            "long_url": url
        }
    )
    response.raise_for_status()
    bitlink_result = response.json()
    
    return bitlink_result["link"]

def count_clicks(token, url):
    bitlinks_site = f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary"
    response = requests.get(
        bitlinks_site,
        headers = {
            "Authorization": f"Bearer {token}"
        },
        params = {
            "unit": "day",
            "units": -1
        }
    )
    response.raise_for_status()
    bitlink_result = response.json()
    
    return bitlink_result["total_clicks"]

def is_bitlink(token, url):
    bitlinks_site = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    
    response = requests.get(
        bitlinks_site,
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )
    return response.ok


def main():
    token = os.environ["BITLINK_TOKEN"]
    url = args.link
    urlparsed = urlparse(url).netloc + urlparse(url).path
    if is_bitlink(token, urlparsed):
        try:
            print("Колличество перехождений по ссылке", count_clicks(token, urlparsed))
        except requests.exceptions.HTTPError:
            print("Введена некорректная ссылка")
    else:
        try:
            print("Битлинк", shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print("Введена некорректная ссылка")

if __name__ == "__main__":
    main()
