from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
import lxml


# full "scrape" function, comprised of the four subfunctions
# defined below
def scrape():
    # create the overall dictionary to hold all the results
    # which will be returned by this function to the flask app
    results = {}

    # first, scrape and then add the article info
    article_info = scrape_article_info()
    results.update(article_info)
    print("Article Info Scraped!")

    # scrape and then add the featured mars image
    featured_image = scrape_featured_mars_image()
    results.update(featured_image)
    print("Featured Image Scraped!")

    # scrape and then add the Mars data table
    Martian_data_table = scrape_data_table()
    results.update(Martian_data_table)
    print("Martian Data Table Scraped!")

    # scrape and then add the hemisphere images
    hemisphere_images = scrape_hemisphere_enhanced_images()
    results.update({"Hemispheres":hemisphere_images})
    print("Hemisphere Images Scraped!")

    print(results)
    return results

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

    browser.links.find_by_partial_text("more info").click()

    time.sleep(1)

    #get image src
    img_soup = bs(browser.html, "html.parser")

    img_src = img_soup.find("img", class_="main_image")["src"]
    img_src = base_url + img_src

    browser.quit()

    return {"featured_image": img_src}

# scrape Mars data table info directly from space-facts.com/mars
def scrape_data_table():
    data_table_url = "https://space-facts.com/mars/"
    tables = pd.read_html(data_table_url)
    mars_info_df = tables[0]
    mars_info_df = mars_info_df.set_index(0)
    mars_info_df.index.name = "Mars"
    mars_info_df.columns = ["Data Table"]
    mars_info_df
    #html_mars_table = mars_info_df.to_html()
    #return
    output_dict = mars_info_df.to_dict()

    return output_dict


# scrape high-quality pictures for each Martian hemisphere
# returns a dictionary of hemisphere name to file location
def scrape_hemisphere_enhanced_images():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    base_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    all_hemispheres = []

    browser.visit(base_url)
    num_hemispheres = len(browser.find_by_css(".thumb"))

    for hemisphere_num in range(num_hemispheres):
        curr_title = browser.find_by_tag(
            "h3")[hemisphere_num].html.replace(" Enhanced", "")
        browser.find_by_css(".thumb")[hemisphere_num].click()
        curr_img_url = browser.find_by_text("Sample").first["href"]
        # print(curr_img_url)
        browser.back()

        all_hemispheres.append({"title": curr_title, "img_url": curr_img_url})

    browser.windows[0].close_others()
    # print(all_hemispheres)
    browser.quit()

    return all_hemispheres
