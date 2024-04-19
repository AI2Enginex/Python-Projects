
import requests
import pandas as pd
from bs4 import BeautifulSoup

class Web_Scrape:

    def __init__(self,file_name,col1,col2,link_name):

        self.df = pd.read_csv(file_name,index_col=col1,encoding='utf-8')
        self.link = link_name
        self.id_val = self.df.index[self.df[col2] == self.link]

    def scrape_data(self,html_tag):

        response = requests.get(self.link)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.paragraphs = self.soup.find_all(html_tag)

    def save_text(self,html_tag,*args):
        
        self.scrape_data(html_tag)

        for data in args:
            for tag in self.soup.find_all(class_ = data):
                tag.decompose()

        with open(str(self.id_val[0])+'.txt','w',encoding='utf-8') as f:
            for p in self.paragraphs:
                f.write(p.text+'\n')
        f.close()

if __name__ == '__main__':

    pass



        



