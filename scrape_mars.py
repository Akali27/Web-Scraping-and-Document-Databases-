
from bs4 import  BeautifulSoup
from splinter import Browser
import pandas as pd
import json
import time
import re 




def scrape():
	# start the splinter browser instance
	browser=Browser('chrome',headless=False)

	# vist  'https://mars.nasa.gov/news/'
	try:
		browser.visit('https://mars.nasa.gov/news/')
		soup_news=BeautifulSoup(browser.html,'lxml')

		news_title=soup_news.find('div',class_='content_title').get_text(strip=True)
		news_p=soup_news.find('div',class_='article_teaser_body').get_text(strip=True)


		# visit 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
		soup_img=BeautifulSoup(browser.html,'lxml')

		url_start='https://www.jpl.nasa.gov'
		# try to do url extraction using regex
		url=soup_img.find('article',class_='carousel_item')['style']
		url_end=re.search('url\(.*',url).group()[5:-3]
		feature_img_url=url_start+url_end

		# visit 'https://twitter.com/marswxreport?lang=en'
		browser.visit('https://twitter.com/marswxreport?lang=en')
		#time.sleep(5)
		soup_weather=BeautifulSoup(browser.html,'lxml')
		mars_weather=soup_weather.find('div',class_='js-tweet-text-container').get_text(strip=True)

		# visit 'http://space-facts.com/mars/'
		browser.visit('http://space-facts.com/mars/')
		#time.sleep(5)
		soup_facts= BeautifulSoup(browser.html,'lxml')
		table_facts= soup_facts.find('table')
		df_facts = pd.read_html(str(table_facts))
		df_facts= json.loads(df_facts[0].to_json())


		# visit 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
		browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
		soup_hd_img_1=BeautifulSoup(browser.html,'lxml')

		# this will gather the images links and titles
		hd_img_title=[]
		hd_img_links=[]
		for url in soup_hd_img_1.select('div.description > a.itemLink.product-item'):
			hd_img_links.append('https://astrogeology.usgs.gov'+url['href'])
			hd_img_title.append(url.get_text(strip=True))

		# this will go to each image link and grab the the high resolution image url
		hd_img_urls=[]
		for url in hd_img_links:
			browser.visit(url)
			#time.sleep(5)
			soup_hd_img_2=BeautifulSoup(browser.html,'lxml')
			hd_img_urls.append(soup_hd_img_2.find("a",text='Sample')['href'])


		key=['title','img_url']
		hemisphere_image_urls=[]
		for i in range(len(hd_img_title)):
			value=[]
			value.append(hd_img_title[i])
			value.append(hd_img_urls[i])
			hemisphere_image_urls.append(dict(zip(key,value)))

		#close the browser
		browser.quit()


		# prepare the dictionary of the data
		key=['news_title','news_p','feature_img_url','df_facts','mars_weather','hemisphere_image_urls']
		value=['-']*6
		value[0]=news_title
		value[1]=news_p
		value[2]=feature_img_url
		value[3]=df_facts
		value[4]=mars_weather
		value[5]=hemisphere_image_urls

		dict_mars=dict(zip(key,value))

		return dict_mars
	except:
		browser.quit()
