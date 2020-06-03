from twitter_scraper import get_tweets
import twitter_scraper
import pandas as pd 
from bs4 import BeautifulSoup as bs
import requests 
import time 
from splinter import Browser 

# url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
# url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
# url3 = "https://space-facts.com/mars/"

# # executable_path = {'executable_path': 'chromedriver.exe'}
# # browser = Browser('chrome', **executable_path, headless=False)


# # def init_browser():   
# #     executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# #     return Browser("chrome", **executable_path, headless=False)

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Nasa
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    news = soup.find("div", class_="list_text")
    title = soup.find("div", class_="content_title").text
    news_p = news.find("div", class_="article_teaser_body").text

    #img
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    html2 = browser.html
    soup = bs(html2, 'html.parser')
    img_link = soup.find('div', class_="carousel_items")
    img_link = img_link.find("article")['style'].split("('", 1)[1].split("')")[0]
    img_url = 'https://www.jpl.nasa.gov' + str(img_link)

    #twitter
    url_3 = "https://twitter.com/marswxreport"
    browser.visit(url_3)
    tweet_html = browser.html
    soup = bs(tweet_html, 'html.parser')
    tweets = []
    for tweet in get_tweets('@MarsWxReport', pages=1):
        twt = tweet['text']
        tweets.append(twt)

    #table
    url4 = "https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ["Category", "Values"]
    html_table = df.to_html()
    html_table.replace("\n", " ")

    #hemis
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
    ]


    scrape_data_dict = {
        "News Title" : title,
        "News Paragraph" : news_p,
        "Image" : img_url,
        "Tweet" : tweets[0],
        "Mars Facts" : html_table,
        "Hemisphere Image URL's" : hemisphere_image_urls
    }
    return scrape_data_dict


