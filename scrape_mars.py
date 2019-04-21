import pandas as pd
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/Eric Tsai/Anaconda3/Library/bin/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    
    ### NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('ul',class_='item_list')

    slides = article.find_all('li')

    title_list = []
    synopsis_list = []

    for slide in slides:
        title = slide.find(class_='content_title').find('a').text
        title_list.append(title)
        synopsis = slide.find(class_='article_teaser_body').text
        synopsis_list.append(synopsis)

    #gather most current title and synopsis
    curr_title = title_list[0]
    curr_synopsis = synopsis_list[0]

    ### JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    picture = soup.find('article',class_='carousel_item')['style']
    #url clean up
    pic_clean_1 = picture.replace('background-image: url(\'', '')
    pic_clean_2 = pic_clean_1.replace('\');','')
    pic_full_url = "https://www.jpl.nasa.gov" + pic_clean_2


    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #get tweet
    tweet = soup.find('div',class_='js-tweet-text-container').find('p').text


    ### Mars Facts
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    planet_table = pd.read_html(url)
    planet_df = planet_table[0]
    planet_df.columns = ['description','value']
    np_df = planet_df.set_index('description')
    np_df.head()
    #turn into html
    planet_html_table = np_df.to_html()
    clean_pht = planet_html_table.replace('\n', '')
    clean_one_pht = clean_pht.replace("'",'')
    clean_one_pht

    ### Mars Hemispheres
    items = []
    image_list = []
    title_list = []
    click_urls = []
    astro_data = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='description')

    for item in items:
        click_urls.append('https://astrogeology.usgs.gov' + item.find('a')['href'])

    try:
        for urls in click_urls:
            browser.visit(urls)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(2)
            title = soup.find('div',class_='content').find('h2',class_='title').text
            title_list.append(title)
            large_image = soup.find('img',class_='wide-image')['src']
            image_list.append('https://astrogeology.usgs.gov' + large_image)
    except ElementDoesNotExist:
        print("Scraping Complete")
        
    for x in range(0,len(title_list)):
        info = {
            "title": title_list[x],
            "img_url": image_list[x],
        }
        astro_data.append(info)

    planet_data = {
    "table":clean_one_pht,
    "tweet":tweet,
    "feat_img":pic_full_url,
    "curr_title":curr_title,
    "curr_synopsis":curr_synopsis,
    "astro_data": astro_data
    }

    browser.quit()

    return planet_data