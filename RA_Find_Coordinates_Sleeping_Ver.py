from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np

# Filter all the warnings.
import warnings
warnings.filterwarnings("ignore")

path = "C:/Users/Lenovo/Desktop/RA/"
df_total = pd.read_stata(path + "lender_cleaned.dta")

# Set the number [num] of each group of lenders, whose coordinates that we
# want to crawl, as well as the start index and end index.
num = 100  # When program has got [num] lenders' coordinates, it will take a rest for about 5 min.
total_num = 100  # total_num = end - start + 1
start = 5501
end = 5600  # end = start + total_num - 1
# file_name_1 = "df_1_{}_{}.dta".format(start, end)
# file_name_2 = "df_2_{}_{}.dta".format(start, end)

# It is better for us to take 50 lenders as one group, and then we can
# get locations (i.e., latitude & longitude) one group by one group.
# The objective of so is to avoid from blocking by Google, since
# it may detect that we are scraping its websites.
# (Yeah, Google does not like users' auto crawling at all.)



# A example of expected url:
# 'https://www.google.com/maps/place/%E5%8D%B0%E5%BA%A6%E5%8F%A4%E5%90%89%E6%8B%89%E7%89%B9%E9%82%A6%E5%8D%A1%E5%A5%87/@23.7124049,69.9228488,8z/data=!3m1!4b1!4m5!3m4!1s0x39511e0750db4489:0x2049bf8ec25dea88!8m2!3d23.7337326!4d69.8597406'
# The function below is defined to extract both latitude and longitude from one expected url.
def get_lat_long(page_url):
    ls = page_url.split('@')[1].split(',')
    latitude = float(ls[0])
    longitude = float(ls[1])
    return latitude, longitude

# Force Google to show website in English.
options = webdriver.EdgeOptions()
options.add_argument('lang=en_US')

# If '/search/' is within current page url, it indicates that we do not get the result.
# Moreover, if we obtain the result successfully, '/place/' must appear in the url scraped by Python.
n_group = int(total_num / num)
path_save = "C:/Users/Lenovo/Desktop/RA/Crawl/"
for j_ in range(n_group):
    start_ = start + j_ * num - 1
    end_ = start + (j_ + 1) * num - 1
    print(start_ + 1)
    print(end_)
    df = df_total.iloc[start_:end_, ]\
        .reset_index(drop=True)
    df['lat'] = np.nan
    df['lon'] = np.nan
    df['flag'] = 1  # 0=unsuccessful, 1=successful

    for i_ in range(num):
        city_ = df.iloc[i_, 1]
        state_ = df.iloc[i_, 2]
        if state_ != "\\n":
            url = 'https://www.google.co.uk/maps/search/' + '{}, {}, India'.format(city_, state_)
        else:
            url = 'https://www.google.co.uk/maps/search/' + '{}, India'.format(city_)

        try:
            driver = webdriver.Edge(executable_path=r"C:\Users\Lenovo\Desktop\RA\MicrosoftWebDriver.exe",
                                options=options)
        except Exception:
            driver = webdriver.Edge(executable_path=r"C:\Users\Lenovo\Desktop\RA\MicrosoftWebDriver.exe",
                                options=options)
        else:
            pass
        # driver.set_window_size(100, 100)
        sleep(8 + np.random.normal(loc=0, scale=1.26))
        try:
            driver.get(url)
        except Exception:
            print('Error occupies, when trying to visit Google.')
            sleep(20 + np.random.normal(loc=0, scale=1.26))
            driver.get(url)
        else:
            pass
        sleep(8 + np.random.normal(loc=0, scale=0.09))
        currentPageUrl = driver.current_url
        # sleep(5 + np.random.normal(loc=-.89, scale=0.89))
        driver.close()

        if ('/search/' not in currentPageUrl) and ('/place/' in currentPageUrl):

            lat, lon = get_lat_long(currentPageUrl)
            df.iloc[i_, 3] = lat
            df.iloc[i_, 4] = lon

        else:

            df.iloc[i_, 5] = 0  # If unsuccessful, set flag = 0
            print('Not Found.')

        if i_ == 50:
            sleep(60)

    df_1 = df[df['flag'] == 1]  # df_1: restore lenders whose locations have been detected
    df_2 = df[df['flag'] == 0]  # df_2: restore lenders whose locations haven't been detected

    file_name_1_ = "df_1_{}_{}.dta".format(start_ + 1, end_)
    file_name_2_ = "df_2_{}_{}.dta".format(start_ + 1, end_)
    df_1.to_stata(path_save + file_name_1_)
    df_2.to_stata(path_save + file_name_2_)

    if j_ < n_group - 1:
        print('Now let us take a rest!')
        sleep(260)
