import logging 

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('davbox')

class Client:
  def __init__(self):
    self.session = requests.Session()
    self.session.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
      'Accept-Language': 'ru',
    }

  def load_page(self):
    url = 'https://davbox.ru/case/free-box'
    res = self.session.get(url=url)
    res.raise_for_status()
    return res.text

  def parse_page(self, text: str):
    soup = BeautifulSoup(text, 'lxml')
    container = soup.select('a.boxes-product-block')
    for block in container:
      self.parse_block(block=block)

  def parse_block(self, block):
    mainblock = block.select_one('div.inner')
    name = mainblock.select_one('div.name') 
    if not name:
      logger.error('no name')
      return
    price = mainblock.select_one('div.price') 
    if not price:
      logger.error('no price')
      return
    percent = mainblock.select_one('div.percent') 
    if not percent:
      logger.error('no percent')
      return
    logger.info('%s, %s, %s', name, price, percent)

  def run(self):
    text = self.load_page()
    self.parse_page(text=text)




if __name__ == "__main__":
  parser = Client()
  parser.run()