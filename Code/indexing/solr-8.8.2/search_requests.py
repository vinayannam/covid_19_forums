from urllib.request import urlopen
from urllib.parse import quote_plus
import json
import ast

runLoop = True
while runLoop:

    # Uncomment to only run once
    # runLoop = False

    term = quote_plus(input('Enter search term: '))

    #######################################################################
    # Query 1: Search for a term across all posts
    #######################################################################
    # uncomment next line to return up to 800 results
    # with urlopen('http://localhost:8983/solr/metamap/select?q={}&rows=800'.format(term)) as url:
    with urlopen('http://localhost:8983/solr/metamap/select?q={}'.format(term)) as u: #return upto 10 results by default
        result1 = json.loads(u.read().decode())
    
    # post_num is the list of post numbers (used for Query 2)
    post_num = []
    # post_url is the list of urls (used for Query 3)
    post_url = []
    for res in result1['response']['docs']:
        post_num.append(res['PostNumber'][0])
        post_url.append(res['PostLink'][0])

    if not post_num:
        print("No results.\n")
        continue
    
    # post_info format: [(post_num1, post_url2), (post_num2, post_url2), ...]
    post_info = list(zip(post_num, post_url))

    #######################################################################
    # Query 2: Get all symptoms/treatments/body parts from a group of posts
    #######################################################################
    unique_num = list(set(post_num))
    symptom_list = []
    treatment_list = []
    drug_list = []
    bodypart_list = []
    for num in unique_num:
        #return upto 10 results by default
        with urlopen('http://localhost:8983/solr/metamap/select?q=PostNumber%3A{}'.format(num)) as u:
            result2 = json.loads(u.read().decode())

        for res in result2['response']['docs']:
            if 'SymptomName' in res.keys():
                symptom_list.append(res['SymptomName'][0])
            elif 'TreatmentName' in res.keys():
                treatment_list.append(res['TreatmentName'][0])
            elif 'DrugName' in res.keys():
                drug_list.append(res['DrugName'][0])
            elif 'BodypartName' in res.keys():
                bodypart_list.append(res['BodypartName'][0])

    print("\nList of related symptom : {}".format(symptom_list))
    print("List of related treatment: {}".format(treatment_list))
    print("List of related drug: {}".format(drug_list))
    print("List of related body part: {}".format(bodypart_list))
    print("\n\n\n")

    #######################################################################
    # Query 3: Get the content, replies, and subreplies of a group of posts
    #######################################################################
    unique_url = list(set(post_url))
    final_results_all = []
    for url in unique_url:
        with urlopen('http://localhost:8983/solr/allData/select?q=url%3A%22{}%22'.format(url)) as u: #return upto 10 results by default
            result3 = json.loads(u.read().decode())
    
        final_results = []
        for res in result3['response']['docs']:
            content = res['content'][0]
            replies = res['replies'][0]
            replies_list = ast.literal_eval(replies)
            
            final_results.append({'url': url, 'content': content, 'replies': replies_list})
            
        # Format of final_results_all: [{url1, content1, replies1}, {url2, content2, replies2}, ...]
        # 'replies' format: {'content', 'sub_replies}
        final_results_all.append(final_results)   

    

    # print out final result
    for url_res in final_results_all:
        for res in url_res:
            url = res['url']
            content = res['content']
            replies = res['replies']
            print("Url: {}".format(url))
            print("Content: {}".format(content))
            for reply in replies:
                print("\tReply: {}".format(reply['content']) )
                for subreply in reply['sub_replies']:
                    if subreply != '':
                        print("\t\tSubreply: {}".format(subreply))
            print("\n")
        print('\n------------------------------------------------------------------------')
