'''this code is used to find the L1A image namelist from the website of NASA with lon-lat csv file
'''

# Load modules
import os
import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import traceback
from dbfread import DBF
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

data_url = "https://oceancolor.gsfc.nasa.gov/cgi/browse.pl?sub=level3&per=CU&day=19783&set=10&ndx=0&mon=19754&sen=amod&rad=0&frc=0&dnm=D@M&prm=TC"
service = Service(executable_path=r'D:\chromedriver\chromedriver.exe')

def getFilelist(w,n,e,s): # return filelist_url,content
    # 无头模式
    option = Options()# Options类实例化
    option.add_argument('--headless')#无头模式后台运行
    driver = webdriver.Chrome(service=service,options=option)
    driver.get(data_url)
    time.sleep(2)

    #n w e s Findswaths 1 2 3 4 5
    xpath_='/html/body/center/form/table/tbody/tr/td[3]/input'
    xpaths=[]
    for i in range(5):
        xpaths.append(xpath_+f'[{i+1}]')
    # print(xpaths)
    args=[n,w,e,s] # n w e s
    print(args)
    # print(type(args[1]))
    # print('input args')
    for i in range(4):
        try:
            element = driver.find_element(By.XPATH, xpaths[i])
            if element.is_enabled():
                element.send_keys(args[i])
            else:
                print("Element is not enabled for interaction")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        # driver.find_element(By.XPATH,xpaths[i]).send_keys(args[i])
        # driver.find_element_by_xpath(xpaths[i]).send_keys(args[i])
        
    driver.find_element(By.XPATH, xpaths[4]).click()
    # print('click Findswaths')
    time.sleep(1)

    # LISTL0xpath='/html/body/center/table[2]/tbody/tr[6]/td[1]'
    LISTxpath='/html/body/center/table[2]/tbody/tr[6]/td[1]/a[1]'
    elem=driver.find_element(By.XPATH,LISTxpath)
    filelist_url=elem.get_attribute("href")

    driver.get(filelist_url)
    # print('click filelist_url')
    # 显式等待页面加载完成
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    elem=driver.find_element(By.TAG_NAME,'body')
    # print(elem)
    content=elem.text
    # print('get content')
    driver.quit()
    return filelist_url,content

def str2csv(filelist_str,outpath):
    lines = filelist_str.split('\n')
    data_dict = {'filename': [line.replace('/', ' ') for line in lines]}
    df = pd.DataFrame(data_dict)
    df.to_csv(outpath,index=False)

def dbf2csv():
    # 读取DBF文件
    table = DBF(r"G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\final\coast_points_f.dbf")

    # 打开CSV文件并写入表头
    with open(r"G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\final\coast_points_f.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=table.field_names)
        writer.writeheader()

        # 将DBF文件的内容写入CSV文件
        for record in table:
            writer.writerow(record)

def main():
    coastp=pd.read_csv(r"G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\coastGrids\coastGridstest.csv")
    outpath_=r'G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\coastfilelist'
    urls=[]
    error_=[]
    fnames=[]
    # df0=pd.DataFrame()
    for i in range(len(coastp)):
        fid=coastp['id'][i]
        w=int(coastp['w'][i])
        n=int(coastp['n'][i])
        e=int(coastp['e'][i])
        s=int(coastp['s'][i])
        print(fid,w,n,e,s)
        try:
            filelist_url,filelist_str=getFilelist(w,n,e,s)
            if len(filelist_str)<1:
                error_.append(1)
            else:
                print('get content---')
                error_.append(0)
            urls.append(filelist_url)
            fname=f'{fid:04d}_{w:.2f}_{n:.2f}.csv'
            fnames.append(fname)
            outpath=os.path.join(outpath_,fname)
            lines = filelist_str.split('\n')
            data_dict = {'filename': [line.replace('/', ' ') for line in lines]}
            df = pd.DataFrame(data_dict)
            df.to_csv(outpath,index=False)
            # df0=pd.concat([df0,df],axis=0)

        except Exception as e:
            traceback.print_exc(file=open(r'G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\coastfilelist\%s_error.txt'%(fid),'a'))
    # df0 = df0.sort_values(by=['filename']).drop_duplicates()
    # df0.to_csv(os.path.join(outpath_,"coastfilelist.csv"),index=False)
    coastp['error']=error_
    coastp['filename']=fnames
    # coastp['filelist_url']=urls
    # coastp.to_csv(r"G:\global_Rrs_L2_hkm_zd\dataset\getcoastfile\coast_filelist_info.csv",index=False)

def main1():
    xpath='/html/body/div[2]/div[2]/div[5]/div[1]/div/form/span[1]/input'
    xpath='//*[@id="kw"]'
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.baidu.com")
    time.sleep(2)
    print('input args')
    try:
        element = driver.find_element(By.XPATH, xpath)
        if element.is_enabled():
            element.send_keys('why send key not working???')
        else:
            print("Element is not enabled for interaction")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    driver.quit()

def main2():
    getFilelist(15,45,30,40)

if __name__ == '__main__':
    main()
    print("done")