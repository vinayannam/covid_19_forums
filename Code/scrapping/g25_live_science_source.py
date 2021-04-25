#Importing the necessary packages
import requests
import random
from bs4 import BeautifulSoup
import json
import tqdm.notebook as tq


#User agents to get rid of bots
discussions = []
for i in tq.tqdm(range(1,9)):
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', ]
    
    #Pick a random user agent
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    
    #Respective URL to be scraped 
    url = "https://forums.livescience.com/forums/"+'coronavirus-epidemiology.42/'+'page-'+str(i)
    
    html_content = requests.get(url, headers=headers)
    
    
    soup = BeautifulSoup(html_content.content, 'html.parser')
    #print(soup)
    
    mydivs = soup.findAll("div", {"class": "structItem-title"})
    thread_list = []
    for div in mydivs:
        temp = div.find('a').get('href')
        thread_list.append(temp)
    
    for i in thread_list:
        url = 'https://forums.livescience.com'+str(i)
        #print(url)
        html_content = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_content.content, 'html.parser')
        title = soup.find("h1", {"class":"p-title-value"})
        discussion = {
                'url': url,
                'Title': title.get_text(),
                'Replies': []
                }
        
        replies = soup.findAll("div",{"class":"bbWrapper"})
        #print("Title:",title.get_text())
        #content = soup.findAll("div",{"class":"bbWrapper"})

        
        for con in replies:
            #print(con.get_text())
            discussion['Replies'].append(con.get_text())
        discussions.append(discussion)
    
out_file = open("covid_discussion.json","w")
json.dump(discussions,out_file,indent=2)
out_file.close()
