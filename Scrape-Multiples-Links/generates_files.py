import pandas as pd
import scraping as sc

file_name = pd.read_csv('Input.csv',encoding='utf-8')
url_list = file_name['URL'].to_list()


for links in url_list:

    file_obj = sc.Web_Scrape('Input.csv',col1='URL_ID',col2='URL',link_name=links)

    file_obj.save_text('p','tdm-descr','tdm_block','td_block_inner')