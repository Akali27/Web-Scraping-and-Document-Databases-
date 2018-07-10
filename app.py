from flask import Flask , render_template
from scrape_mars import scrape
from pymongo import  MongoClient
import pandas as pd

app=Flask(__name__)

@app.route('/scrape')
def scrape_mars():
	dict_mars=scrape()
	# this will start the mongodb client
	if dict_mars is not None:
		client=MongoClient()
		db=client.mars_data
		db.get_collection('mars_dictionary').drop()
		collection_mars=db.mars_dictionary
		collection_mars.insert_one(dict_mars)
		return "YES"
	else:
		return "NO"



@app.route('/')

def display_mars():
	# # this will start the mongodb client
	client=MongoClient()
	db=client.mars_data
	# geting data from mongodb
	mars_dictionary=db.get_collection('mars_dictionary').find_one()
	df=mars_dictionary['df_facts']
	df=pd.DataFrame(df)
	mars_facts_table=df.to_html(header=False,index=False)
	feature_img_url=mars_dictionary['feature_img_url']
	mars_weather=mars_dictionary['mars_weather']
	news_p=mars_dictionary['news_p']
	news_title=mars_dictionary['news_title']
	hemisphere_image_urls=mars_dictionary['hemisphere_image_urls']
	url_title_0=hemisphere_image_urls[0]
	url_0=url_title_0['img_url']
	title_0=url_title_0['title']
	url_title_1=hemisphere_image_urls[1]
	url_1=url_title_1['img_url']
	title_1=url_title_1['title']
	url_title_2=hemisphere_image_urls[2]
	url_2=url_title_2['img_url']
	title_2=url_title_2['title']
	url_title_3=hemisphere_image_urls[3]
	url_3=url_title_3['img_url']
	title_3=url_title_3['title']
	
	return render_template('index.html', feature_img_url=feature_img_url, mars_facts=str(mars_facts_table),
		mars_weather=mars_weather, news_p=news_p, news_title=news_title,url_0=url_0, title_0=title_0,
		url_1=url_1, title_1=title_1, url_2=url_2, title_2=title_2, url_3=url_3, title_3=title_3
		)
