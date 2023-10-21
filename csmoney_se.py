from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

path = "c:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(path)

def search(search_item, driver):
  # driver.get("https://skinsmonkey.com/trade")
  driver.get(f"https://cs.money/csgo/trade/?search={search_item}&sort=float&order=asc&exterior=Field-Tested")
  time.sleep(10)
  # print(driver.title)
  # temp = driver.find_element_by_class_name('inventory-grid')
  # search = driver.find_element_by_class_name('form-input__core')
  # search.send_keys("asiimov")
  # search.send_keys(Keys.RETURN)
  # print(temp)
  # print(driver.page_source)

  arr = []
  try:
    container = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'bot-listing_body__3xI0X'))
      )
    # print(container)
    items = container.find_elements_by_class_name('actioncard_wrapper__3jY0N')
    for i, item in enumerate(items):
      # print(i, item)
      fv = item.find_element_by_class_name('BaseCard_description__31IqW')
      price = item.find_element_by_class_name('BaseCard_price__27L2x')
      fv = fv.text.split('/')[-1].strip()
      price = price.text.replace('฿','').strip().replace(' ',',') + ' ฿'
      # print(i, fv, price)

      # link = item.find_element_by_tag_name('a')
      # link.click()
      # page_item = WebDriverWait(driver, 10).until(
      # EC.presence_of_element_located((By.CLASS_NAME, 'TradeSkinBanner_wrapper__bMihv'))
      # )

      # fv = page_item.find_element_by_class_name('PropertiesBlock_properties__value__3WzH8')
      # print(fv.text)
      arr.append({'Float':fv, 'Price':price})
  except:
    pass
  df = pd.DataFrame(arr)
  print(df.head(5))
  return driver

if __name__ == '__main__':
  search_list = ['AWP Asiimov', 'AWP Containment breach', 'FAMAS Mecha industries']
  for i in search_list:
    print('-'*50)
    print('>>>', i)
    search_item = i.replace(' ','%20')
    driver = search(search_item,driver)

  driver.quit()
  
