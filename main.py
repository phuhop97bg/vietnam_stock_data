
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
from selenium import webdriver




def get_data(ticker_symbols):
    # driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

    driver.get('https://dstock.vndirect.com.vn/');
    time.sleep(2.5)
    driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/button").click()
    time.sleep(1) # Let the user actually see something!
    driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div/div/div[2]/form/div/input").click()
    for ticker_symbol in ticker_symbols:
            driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div/div/div[2]/form/div/input").send_keys(ticker_symbol)
            driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div/div/div[2]/form/div/div").click()
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[@id="___reactour"]/div[4]/div/button').click()
            except:
                print("")
            current = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div").text
            refer=driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[4]/div[2]").text
            volume= driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]").text
            volume=int(volume.replace(",",""))
            volatility=float(current)-float(refer)
            volatility_percent=float(volatility)/float(refer)*100
            yield float(current); yield float(refer); yield  float(volatility);yield round(volatility_percent,2); yield volume
ticker_symbols=["VNM","HPG","HSG","AMD","FLC"]
n=len(ticker_symbols)

data=list(get_data(ticker_symbols))

data=np.array(data)
data=data.reshape(n,-1)
parameters=["current","refer","volatility","volatility_percent","volume"]

df=pd.DataFrame(data, columns=parameters)
df['symbol']=ticker_symbols
df=df.reindex(columns=["symbol",*parameters])
print(df)