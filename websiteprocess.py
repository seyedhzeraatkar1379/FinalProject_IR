!pip3 install newspaper3k
import requests
from bs4 import BeautifulSoup
import pandas
from newspaper import Article
import numpy
from tqdm import tqdm

# we cNon
general_Links = []
subgeneral_link = []
error_links = []
scraped_data = []

def getgeneralpage_textlink(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    navtutorial = soup.select_one('nav#nav_tutorials')
    navrefrence = soup.select_one('nav#nav_references')
    navexercise = soup.select_one('nav#nav_exercises')
    tutorial_links = navtutorial.select('a');
    refrence_links = navrefrence.select('a');
    exercise_links = navexercise.select('a');
    urlc = url[:-1]
    for l in tutorial_links:
        if(str(l['href']).startswith('/')):
            general_Links.append(urlc+l['href'])
            subgeneral_link.append(urlc+l['href'])
    #for l in refrence_links:
    #    if(str(l['href']).startswith('/')):
    #        general_Links.append(urlc+l['href'])
    #for l in exercise_links:
    #    if(str(l['href']).startswith('/')):
    #        general_Links.append(urlc+l['href'])
    #tgp = soup.select_one('div#main')#txtgeneralpage = tgp.select('h1,h2,h3,h4,h5,h6,p')#for i in txtgeneralpage:
           
def getsubpage_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        #mainbody = soup.select_one('div#main')#mainbody = mainbody.select('h1,h2,h3,h4,h5,h6,p')#if mainbody == None :#    error_links.append(url)#    return#for i in mainbody:#00000000000000000
        links = soup.select_one('div#leftmenuinnerinner')
        if links == None : 
            error_links.append(url)
            return
        links = links.select('a')
        if links == None : 
            error_links.append(url)
            return
        for link in links:
            if (str(link['href']).startswith('/')):
                urlcc = str(url).replace((str(url).split('/'))[-1],'')
                urlcc = urlcc[:-1]
                subgeneral_link.append(str(urlcc)+str(link['href']))
            else:
                urlcc = str(url).replace((str(url).split('/'))[-1],'')
                subgeneral_link.append(str(urlcc)+str(link['href']))
    except:
        error_links.append("Page error: "+url)
def crawl():
    getgeneralpage_textlink("https://www.w3schools.com/")
    for gl in tqdm(general_Links):
        getsubpage_link(gl)
        #print(gl)
    save();
        
def save():
    subgeneral_link.sort()
    for gl in tqdm(subgeneral_link):
        try:
            article = Article(gl)
            article.download()
            article.parse()
            scraped_data.append({'url':gl,'text':article.text,'title':article.title})
        except:
            error_links.append("Page error: "+gl)
    df = pandas.DataFrame(scraped_data)
    df.to_csv("data.csv")    
    
if __name__ == "__main__":
    crawl()
    for i in error_links:
        print(i)