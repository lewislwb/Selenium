import csv
import time
import re
from selenium  import webdriver
from selenium.webdriver.common.keys import Keys   
from selenium.common.exceptions import NoSuchElementException  ###导入异常属性


option = webdriver.ChromeOptions()

option.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options = option)#Chrome driver地址

url='http://hotels.ctrip.com/hotel/shenyang451#ctm_ref=ctr_hp_sb_lst' #携程网址
driver.get(url)
time.sleep(2)

button=driver.find_element_by_css_selector('#appd_wrap_close')
button.click()
time.sleep(2)


tStart=driver.find_element_by_id('txtCheckIn')
tStart.send_keys(Keys.BACKSPACE)
tStart.send_keys(Keys.BACKSPACE)
tStart.send_keys('24')

tExit=driver.find_element_by_id('txtCheckOut')
tExit.send_keys(Keys.BACKSPACE)
tExit.send_keys(Keys.BACKSPACE)
tExit.send_keys('30')

timeClick=driver.find_element_by_id('btnSearch')
timeClick.send_keys(Keys.ENTER)

time.sleep(2)



driver.execute_script('window.scrollBy(0,5800)')
time.sleep(2)


#jump_button=driver.find_element_by_css_selector('.c_page_num')
#jump_button.send_keys(Keys.BACKSPACE)
#jump_button.send_keys('开始的页码')
#jump_button1=driver.find_element_by_css_selector('.c_page_submit')
#jump_button1.send_keys(Keys.ENTER)
page=driver.find_element_by_css_selector('#page_info > div.c_page_list.layoutfix > a:nth-child(9)')  ###定位总页数


for m in range(int(page.text)+2) :
    if m :
        next_button=driver.find_element_by_css_selector('.c_down')       
        next_button.send_keys(Keys.ENTER)
    driver.execute_script('window.scrollBy(0,5800)')
    time.sleep(3)    
 
    html = driver.execute_script("return document.documentElement.outerHTML")
    location = re.findall(r'12[2,3].\d{4,}\W4[1,2].\d{4,}',html) #目标城市经纬度范围
    m=[]
    n=[]
    for i in location:
        i = i.split('|',1)
        if len(m) != 0 and i[0] == m[len(m)-1]:
            continue
        else:
            m.append(i[0])
            n.append(i[1])

    infor=driver.find_element_by_css_selector('#hotel_list').find_elements_by_class_name('hotel_new_list')
    for data in infor :
        try:
            recommend=data.find_element_by_css_selector(' ul > li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.recommend').text
        except NoSuchElementException :
            recommend=' '

        try:
            score=data.find_element_by_css_selector('ul > li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.hotel_value').text
        
        except NoSuchElementException :
            score=' '

        try:
            price=data.find_element_by_css_selector('ul > li.hotel_price_icon > div > div > div > a > span').text
        except NoSuchElementException :
            price=' '
        
            
        hotel_information= [data.find_element_by_css_selector(' ul > li.pic_medal > div > a').get_attribute('title'),
                            
        data.find_element_by_css_selector(' ul > li.hotel_item_name > p.hotel_item_htladdress').text.rstrip('地图'and'地图街景') ,
        
        score,
    
        price,
 
        recommend,

        m[0],

        n[0]
        ]

        m.remove(m[0])
        n.remove(n[0])
        
        out = open("/Users/wenboliu/Desktop/_hotel.csv", "a", encoding='UTF-8')
        csv_writer = csv.writer(out, dialect = "excel")
        csv_writer.writerow(hotel_information)
    print('Crawling...')


