from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from robots import RobotsParser
import datetime
import hashlib
import os
import requests
import time
import yaml

class SpecimenAnalyser:

  id = None
  robotParser = None
  driver = None
  folder_path = None
  items = []
  htpass = None
  baseUrl = None

  def __init__(self, id, baseUrl, robots, htpass = None):
    self.id = id
    self.baseUrl = baseUrl
    self.htpass = htpass
    self.folder_path = f'data/{self.id}'
    os.makedirs(self.folder_path, exist_ok = True)
    robotFile = requests.get(baseUrl + robots)
    if robotFile.status_code == 200:
      self.robotParser = RobotsParser.from_string(robotFile.text)

  def checkUrl(self, userAgent, path):
    if self.robotParser != None:
      return self.robotParser.can_fetch(userAgent, path)
    return False

  def loadPage(self, url):
    if self.driver == None:
      options = Options()
      options.add_argument('--headless')  # Ejecución sin interfaz gráfica
      driver = webdriver.Firefox(options = options)
    if self.htpass != None:
      driver.get(url.replace('https://', f'https://{self.htpass["user"]}:{self.htpass["pass"]}@'))
    else:
      driver.get(url)
    time.sleep(10)
    return driver.page_source

  def addLink(self, url):
    # if not site.checkUrl('spider:aa', '/'):
    #   return []
    if url == '/':
      url = self.baseUrl
    elif 'sites/default/files' in url:
      return []
    elif url.startswith('/'):
      url = self.baseUrl + url
    elif url.startswith(self.baseUrl):
      pass
    else:
      return []
    file_path = self.urlToFile(url)
    print(url, file_path)
    # return ['/Blackboard_Data']
    if not os.path.isfile(file_path):
      with open(file_path, 'w') as file:
        content = self.loadPage(url)
        file.write(content)
        file.close()
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)
        return set(link['href'] for link in links)
    return []

  def urlToFile(self, url):
    url = url.replace(specimen['base_url'], '')
    url = url[:url.find('?')]
    parts = url.split('/')
    if len(parts) == 0 or (len(parts) == 1 and parts[0] == ''):
      return self.folder_path + '/index.html'
    else:
      os.makedirs(self.folder_path + '/'.join(parts), exist_ok = True)
      return self.folder_path + '/'.join(parts)  + '/index.html'

  def close(self):
    self.driver.close()

with open('specimens.yml', 'r') as file:
  config = yaml.safe_load(file)

for specimen in config['specimens']:
  site = SpecimenAnalyser(specimen['id'], specimen['base_url'], '/robots.txt', specimen['htpass'])
  pages = site.addLink('/')
  while len(pages) > 0:
    url = pages.pop()
    links = site.addLink(url)
    pages = list(pages) + list(links)
    pages = list(dict.fromkeys(pages))
    # break
  # site.close()
  # break
