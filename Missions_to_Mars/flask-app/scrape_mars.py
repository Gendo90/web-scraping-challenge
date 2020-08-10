from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def scrape():
    return None

# first scraped info for the Mars app, article headline and summary
# from the NASA website, returned as a dictionary
def scrape_article_info():
    url = "https://mars.nasa.gov/news/"

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    browser.visit(url)

    mars_news = browser.html

    news_soup = bs(mars_news, "html.parser")

    latest_news = news_soup.find_all("li", class_="slide")[0]

    latest_headline = latest_news.find("div", class_="content_title").a.text
    latest_description = latest_news.find("div", class_="article_teaser_body").text

    browser.quit()

    return {"headline":latest_headline, "description":latest_description}


# scrape the latest Mars image from the JPL website, returned as a dictionary
def scrape_featured_mars_image():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    base_url = "https://www.jpl.nasa.gov"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(image_url)
    browser.find_by_css('img.thumb').first.click()

    time.sleep(2)
    browser.execute_script(
        "document.getElementById('fancybox-lock').scrollTo(0, document.body.scrollHeight);")

    browser.click_link_by_partial_text("more info")

    time.sleep(1)

    #get image src
    img_soup = bs(browser2.html, "html.parser")

    img_src = img_soup.find("img", class_="main_image")["src"]
    img_src = base_url + img_src
    return {"featured_image": img_src}

