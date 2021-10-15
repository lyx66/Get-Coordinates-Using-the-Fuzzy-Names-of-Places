from selenium import webdriver
from time import sleep
import pandas as pd
from tqdm import tqdm

path = "C:/Users/Lenovo/Desktop/RA/"
df = pd.read_stata(path + "save_1后尚未被提取的.dta")

# Filter all the warnings.
import warnings
warnings.filterwarnings("ignore")


# A example of expected url:
# 'https://www.google.com/maps/place/%E5%8D%B0%E5%BA%A6%E5%8F%A4%E5%90%89%E6%8B%89%E7%89%B9%E9%82%A6%E5%8D%A1%E5%A5%87/@23.7124049,69.9228488,8z/data=!3m1!4b1!4m5!3m4!1s0x39511e0750db4489:0x2049bf8ec25dea88!8m2!3d23.7337326!4d69.8597406'
# The function below is defined to extract both latitude and longitude from one expected url.
def get_lat_long(page_url):
    ls = page_url.split('@')[1].split(',')
    latitude = ls[0]
    longitude = ls[1]
    return latitude, longitude


driver = webdriver.Edge(executable_path=r"C:\Users\Lenovo\Desktop\RA\MicrosoftWebDriver.exe")
Url_With_Coordinates = []

url = 'https://www.google.com/maps/search/' + '{}, India'.format('Kutch')
driver.get(url)
sleep(3)
currentPageUrl = driver.current_url

# If '/search/' is within current page url, it indicates that we do not get the result.
# Moreover, if we obtain the result successfully, '/place/' must appear in the url scraped by Python.
if ('/search/' not in currentPageUrl) and ('/place/' in currentPageUrl):
    Url_With_Coordinates.append(currentPageUrl)

lat, long = get_lat_long(currentPageUrl)
