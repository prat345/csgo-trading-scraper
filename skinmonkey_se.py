from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re


def open_site():
  path = "c:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
  driver = webdriver.Chrome(path)
  driver.maximize_window()
  driver.get("https://skinsmonkey.com/trade")
  # driver.implicitly_wait(10)
  time.sleep(5)
  site = driver.find_element("xpath", "//div[contains(@class, 'trade-inventory')][contains(@data-inventory, 'SITE')]")
  return driver, site

def item_exterior():
  # select condition
  filter = driver.find_element("xpath", "//div[contains(@class, 'trade-panel')]")
  exterior = filter.find_element("xpath", "//div[contains(@class, 'trade-collapse trade-filter-exterior')]")
  action = ActionChains(driver).move_to_element(exterior)
  action.click(exterior)
  action.perform()
  time.sleep(2)
  driver.implicitly_wait(2)

  checkboxs = driver.find_elements("xpath", "//div[contains(@class, 'trade-filter-option__box')]")
  print([i.get_attribute('innterText') for i in list(checkboxs)])
  FT = checkboxs[3]
  print(FT)
  action = ActionChains(driver).move_to_element(FT)
  action.click(FT)
  action.perform()
  time.sleep(2)

def item_sort(site):
  # select sorting
  sort = site.find_elements("xpath","//div[contains(@label, 'Sort')]")[-1]
  action = ActionChains(driver).move_to_element(sort)
  action.click(sort)
  action.perform()
  time.sleep(1)
  orderlist = sort.find_element("xpath", "//div[contains(@class, 'select-list')]")
  order = orderlist.find_elements("xpath", "//div[contains(@class, 'select-item')]")[-1] # min float
  action = ActionChains(driver).move_to_element(order)
  action.move_to_element(order)
  action.click(order)
  action.perform()
  time.sleep(2)

def item_searchbar(search_item, site):
  links = site.find_elements("xpath", "//input[contains(@placeholder, 'Search inventory…')][contains(@class, 'form-input__core')]")
  search = links[-1]
  action = ActionChains(driver).move_to_element(search)
  # action.click(search)
  action.double_click(search).click_and_hold(search).send_keys(Keys.CLEAR)
  action.send_keys(search_item)
  action.perform()
  time.sleep(1)
  submit = site.find_element("xpath", "//div[contains(@id, 'search-phrase')][contains(@class, 'search-results__phrase')]")
  action = ActionChains(driver).move_to_element(submit)
  action.click(submit)
  action.perform()
  time.sleep(2)

def format_time(text):
    text = text.replace('Locked for ', '')
    # days = '0'
    # if 'days' in text:
    #   days = int(re.search(r'(\d+) day', text).group(1))
    # hours = int(re.search(r'(\d+) hr', text).group(1))
    # minutes = int(re.search(r'(\d+) min', text).group(1))
    # text = "{} days, {:02d} hr".format(days, hours, minutes)
    return text

def search(search_item, driver, site):
  item_searchbar(search_item, site)
  item_sort(site)

  arr = []
  try:
    container = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'vue-recycle-scroller__item-wrapper'))
      )
    # container = container.find_elements('xpath', "//div[contains(@class, 'vue-recycle-scroller__item-wrapper')]")
    # print(container.get_attribute('innerHTML'))
    # items = container.find_elements('xpath', "//div[contains(@class, 'item-card item-card--730')]")
    btns = container.find_elements('xpath', "//div[contains(@class, 'item-card__action item-card__action--info')]")
    for i, btn in enumerate(btns):
      if i > 4: break
      action = ActionChains(driver)
      # action.move_to_element(items[i])
      action.move_to_element(btn)
      time.sleep(2)
      driver.implicitly_wait(5)
      action.click(btn)
      action.perform()

      item_page = site.find_element('xpath',"//div[contains(@class, 'item-details item-details--730')]")
      fv = item_page.find_element('xpath', "//span[contains(@class, 'item-details-param__value')]")
      fv = fv.get_attribute('innerText').strip('\n')
      price = item_page.find_element('xpath', "//div[contains(@class, 'item-price large')]")
      price = price.get_attribute('innerText').strip('\n')
      name = item_page.find_element('xpath', "//div[contains(@class, 'item-params item-details-name__params')]")
      name = name.get_attribute('innerText').strip('\n')
      lock = item_page.find_element('xpath', "//div[contains(@class, 'item-details-lock item-details__lock item-details__lock--desktop')]")
      lock = lock.get_attribute('innerText').strip('\n')

      close = item_page.find_element('xpath',"//div[contains(@class, 'modal__close')][contains(@role, 'button')]")
      action = ActionChains(driver).move_to_element(close)
      action.click(close)
      action.perform()

      # print(i, fv, price)
      arr.append({'Float':fv, 'Price':price, 'Name':name, 'Lock':lock})

  except Exception as e:
    print(e)

  df = pd.DataFrame(arr)
  df['Lock'] = df['Lock'].apply(lambda t: format_time(t))
  print(df)
  return driver, df, df['Float'].min()

def exec():
  global driver
  driver, site = open_site()
  item_exterior()
  sum = {}
  for i in ['AWP Asiimov', 'AWP Containment breach', 'FAMAS Mecha industries']:
    try:
      print('-'*100)
      print('>>>', i)
      driver, df, min_float = search(i, driver, site)
      print('min float: ', min_float)
      sum[i] = df
      # driver.refresh()
    except Exception as e:
      print(e)

  driver.quit()
  return sum

if __name__ == "__main__":
  sum = exec()
  