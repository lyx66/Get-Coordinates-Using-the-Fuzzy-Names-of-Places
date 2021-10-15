from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np

# Filter all the warnings.
import warnings
warnings.filterwarnings("ignore")

path = "C:/Users/Lenovo/Desktop/RA/"
df_total = pd.read_stata(path + "save_1后尚未被提取的.dta")

# Set the number [num] of each group of lenders, whose coordinates that we
# want to crawl, as well as the start index and end index.
num = 10
start = 1
end = 10  # end = start + num - 1

# It is better for us to take 50 lenders as one group, and then we can
# get locations (i.e., latitude & longitude) one group by one group.
# The objective of so is to avoid from blocking by Google, since
# it may detect that we are scraping its websites.
# (Yeah, Google does not like users' auto crawling at all.)
df = df_total.iloc[start - 1:end, ].reset_index(drop=True)
df['lat'] = np.nan
df['lon'] = np.nan
df['flag'] = 1  # 0=unsuccessful, 1=successful


# A example of expected url:
# 'https://www.google.com/maps/place/%E5%8D%B0%E5%BA%A6%E5%8F%A4%E5%90%89%E6%8B%89%E7%89%B9%E9%82%A6%E5%8D%A1%E5%A5%87/@23.7124049,69.9228488,8z/data=!3m1!4b1!4m5!3m4!1s0x39511e0750db4489:0x2049bf8ec25dea88!8m2!3d23.7337326!4d69.8597406'
# The function below is defined to extract both latitude and longitude from one expected url.
def get_lat_long(page_url):
    ls = page_url.split('@')[1].split(',')
    latitude = float(ls[0])
    longitude = float(ls[1])
    return latitude, longitude

# If '/search/' is within current page url, it indicates that we do not get the result.
# Moreover, if we obtain the result successfully, '/place/' must appear in the url scraped by Python.

for i_ in range(num):
    city_ = df.iloc[i_, 1]
    state_ = df.iloc[i_, 2]
    if state_ != "\n":
        url = 'https://www.google.com/maps/search/' + '{}, {}, India'.format(city_, state_)
    else:
        url = 'https://www.google.com/maps/search/' + '{}, India'.format(city_)

    driver = webdriver.Edge(executable_path=r"C:\Users\Lenovo\Desktop\RA\MicrosoftWebDriver.exe")
    # driver.set_window_size(100, 100)
    sleep(3)
    driver.get(url)
    sleep(6.1 + np.random.normal(loc=0, scale=0.89))
    currentPageUrl = driver.current_url
    sleep(5 + np.random.normal(loc=-.89, scale=0.89))
    driver.close()

    if ('/search/' not in currentPageUrl) and ('/place/' in currentPageUrl):

        lat, lon = get_lat_long(currentPageUrl)
        df.iloc[i_, 3] = lat
        df.iloc[i_, 4] = lon

    else:

        df.iloc[i_, 5] = 0

    sleep(2)

df_1 = df[df['flag'] == 1]  # df_1: restore lenders whose locations have been detected
df_2 = df[df['flag'] == 0]  # df_2: restore lenders whose locations haven't been detected
# df_1.to_stata('TEST.dta')
