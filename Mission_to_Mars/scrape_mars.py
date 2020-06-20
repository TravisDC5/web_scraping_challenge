from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time



mars_data = {}

def init_browser():
    
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path)



def mars_news():

    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    headlineElement = news_soup.select_one("ul.item_list li.slide")
    headlineElement.find("div", class_="content_title")

    # Scrape the Latest News Title
    news_title = headlineElement.find("div", class_="content_title").get_text()

    # Scrape the Latest Paragraph Text
    news_paragraph = headlineElement.find("div", class_="article_teaser_body").get_text()
   
    browser.quit()
    return news_title, news_paragraph


    


def mars_image():

    browser = init_browser()
    jplUrl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jplUrl)
    time.sleep(1)

    browser.click_link_by_id('full_image')
    moreInfoButton = browser.links.find_by_partial_text('more info')
    moreInfoButton.click()

    jplHtml = browser.html
    jpl_image = BeautifulSoup(jplHtml, "html.parser")
    jpl_image_url = jpl_image.select_one("figure.lede a img").get("src")
    jpl_image_url = f"https://www.jpl.nasa.gov/{jpl_image_url}"

    
    browser.quit()
    return jpl_image_url
    
    


def mars_weather():

    browser = init_browser()
    weatherUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weatherUrl)
    time.sleep(1)

    weatherHtml = browser.html
    weatherSoup = BeautifulSoup(weatherHtml, 'html.parser')

    latestTweets = weatherSoup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    for tweet in latestTweets: 
        weatherTweet = tweet.find('span').text
        if 'InSight' in weatherTweet:
            weatherTweet
            break
        else: 
            pass

    
    browser.quit()
    return weatherTweet

    

def mars_facts():

    factsUrl = "https://space-facts.com/mars/"
    marsFacts_df = pd.read_html(factsUrl)[0]
    marsFacts_df.columns=["Description", "Value"]
    marsFacts_df.set_index("Description", inplace=True)
    marsFacts = marsFacts_df.to_html()     
    marsFacts2 = marsFacts.replace('<tr style="text-align: right;">','<tr style="text-align: left;">') 
    return marsFacts2


def mars_hemi():

    browser = init_browser()
    hemisphereUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphereUrl)
    time.sleep(1)

    htmlHemispheres = browser.html
    hemisphereSoup = BeautifulSoup(htmlHemispheres, 'html.parser')

    imageAndTitle = hemisphereSoup.find_all('div', class_='item')

    # This list name was supplied to us
    hemisphere_image_urls = []

    hemisphereMainUrl = 'https://astrogeology.usgs.gov'

    for i in imageAndTitle: 
    
        # Grabs the title for each image
        title = i.find('h3').text.replace("Enhanced", "")       
    
        partialImgUrl = i.find('a', class_='itemLink product-item')['href']  
        browser.visit(hemisphereMainUrl + partialImgUrl)      
        partialImgHtml = browser.html       
    
        soup = BeautifulSoup( partialImgHtml, 'html.parser')
        imgUrl = hemisphereMainUrl + soup.find('img', class_='wide-image')['src']
    
        # This appends the supplied list that was given to us
        hemisphere_image_urls.append({"title" : title, "img_url" : imgUrl})
    
    browser.quit()
    return hemisphere_image_urls

    
def scrape():
    
    news_title, news_paragraph = mars_news()
    jpl_image_url = mars_image()
    weatherTweet = mars_weather()
    marsFacts2 = mars_facts()      
    hemisphere_image_urls = mars_hemi()
    mars_data = { 
                'headline': news_title,
                'paragraph': news_paragraph,
                'SpaceImages': jpl_image_url,
                'MarsWeather': weatherTweet,
                'MarsFacts': marsFacts2,
                'MarsHemi': hemisphere_image_urls
            }
    
    return mars_data

#print(scrape())
