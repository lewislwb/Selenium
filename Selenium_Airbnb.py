import csv
import time
import re
from selenium  import webdriver
from selenium.webdriver.common.keys import Keys   
from selenium.common.exceptions import NoSuchElementException  ###导入异常属性


option = webdriver.ChromeOptions()

option.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options = option) #Chrome driver地址

url='https://www.airbnb.cn/s/中国辽宁省沈阳市/homes?query=中国辽宁省沈阳市&place_id=ChIJtzQTOkE8JV4RZpGSzvDkmVQ&checkin=2019-03-24&checkout=2019-03-30&refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&s_tag=vYt27uvH'
driver.get(url)

for i in range(20):
    time.sleep(1)
    rent_list = driver.find_elements_by_css_selector("a._1fp8y05c")
    for eachhouse in rent_list:
        name = eachhouse.find_element_by_css_selector('div._1m9t1a27')
        price = eachhouse.find_element_by_css_selector('span._ppgibgk')
        price = re.search(r'￥(\d{2,5})',price.text).group(1)
   
        try:
            star = eachhouse.find_element_by_xpath(".//span[@class='_q27mtmr']/span[1]").get_attribute('aria-label')
            if star[4] == '.':
                star = star[3:6]
            else:
                star = star[3]
        except:
            star = ' '

        try:
            numreview = eachhouse.find_element_by_css_selector('span._16hhykwk')
            numreview = numreview.text
        except:
            numreview = ' '

    
        try:
            eachhouse.find_element_by_css_selector('div._e296pg').click()
        except:
            try:
                name.send_keys(Keys.ENTER)
            except:
                eachhouse.find_element_by_css_selector('span._z1pr8k6').send_keys(Keys.ENTER)
                
                    
        time.sleep(1)

        m_handle = driver.current_window_handle
        handles = driver.window_handles
        new_handle = None
        
        for handle in handles:
            if handle != m_handle:
                new_handle = handle
        driver.switch_to.window(new_handle)

        time.sleep(1)
        html = driver.execute_script("return document.documentElement.outerHTML")
        try:
            location = re.search(r'location=1\d\d.\d{1,},\d\d.\d{1,}',html).group()
            location = location.split('=',1)
            location = location[1].split(',',1)       
            longtitute = location[0]
            altitute = location[1]
        except:
            longtitute = ' '
            altitute = ' '          
        driver.close()
        driver.switch_to.window(m_handle)
    
        hotelinformation = [name.text, price, star, numreview,longtitute,altitute]
        print(hotelinformation)
        out = open("/Users/wenboliu/Desktop/Shenyang_airbnb.csv", "a", encoding='UTF-8')
        csv_writer = csv.writer(out, dialect = "excel")
        csv_writer.writerow(hotelinformation)
        
        if int(i) == 0:           
            driver.execute_script("window.scrollBy(0,85)","")
        else:
            driver.execute_script("window.scrollBy(0,54)","")
            
    driver.execute_script("window.scrollBy(0,5000)","")           
    time.sleep(1)
    nextBtn = driver.find_elements_by_css_selector('div._1yofwd5')
    if int(i) == 0:
        nextBtn[0].click()
    else:
        nextBtn[1].click()
                
                

    
        
    







