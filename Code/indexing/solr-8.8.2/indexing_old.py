from urllib.request import urlopen
from urllib.parse import quote_plus
from collections import defaultdict
import ast
import json

query = quote_plus(input('Enter query to be searched:'))

def search(query):
	with urlopen('http://localhost:8983/solr/metamap/select?q={}'.format(query)) as u:
		output_1 = json.loads(u.read().decode())
	post_num = []
	post_link = []
	for val in output_1['response']['docs']:
	    post_num.append(val['PostNumber'][0])
	    post_link.append(val['PostLink'][0])
	post_output = list(zip(post_num, post_link))
	print("Relevant post numbers and links for the query")
	print(post_output)
	get_keywords(post_num)
	comments(post_link)

def get_keywords(post_num):
	unique_num = list(set(post_num))
	symptoms = []
	treatments = []
	drugs = []
	bodyparts = []
	for num in unique_num:
	    with urlopen('http://localhost:8983/solr/metamap/select?q=PostNumber%3A{}'.format(num)) as u:
	        output_2 = json.loads(u.read().decode())

	    for val in output_2['response']['docs']:
	        if 'SymptomName' in val.keys():
	            symptoms.append(val['SymptomName'][0])
	        elif 'TreatmentName' in val.keys():
	            treatments.append(val['TreatmentName'][0])
	        elif 'DrugName' in val.keys():
	            drugs.append(val['DrugName'][0])
	        elif 'BodypartName' in val.keys():
	            bodyparts.append(val['BodypartName'][0])
	print("\nRelated symptoms are : {}".format(set(symptoms))) if symptoms else print("No symptoms found")
	print("Related treatments are: {}".format(set(treatments))) if treatments else print("No treatments found")
	print("Related drugs are: {}".format(set(drugs))) if drugs else print("No drugs found")
	print("Related body parts are: {}".format(set(bodyparts))) if bodyparts else print("No related bodyparts found")

def comments(post_link):
	all_links = list(set(post_link))
	reply_dict = defaultdict(int)
	for link in all_links:
	    with urlopen('http://localhost:8983/solr/scrappedData/select?q=url%3A%22{}%22'.format(link)) as u: 
	        output_3 = json.loads(u.read().decode())
	    post_link = []
	    for res in output_3['response']['docs']:
	    	replies = res['replies'][0]
	    	post_link = (res['url'][0])
	    	replies_list = ast.literal_eval(replies)
	    	replies_count = len(replies_list)
	    	reply_dict[post_link] = replies_count
	sorted_urls = sorted(reply_dict.items(), key = lambda x:x[1], reverse = True)
	print("\n")
	print("URLs sorted in descending order according to the count of replies")  
	print(sorted_urls)
search(query)
