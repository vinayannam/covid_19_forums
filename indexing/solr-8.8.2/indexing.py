from urllib.request import urlopen
from urllib.parse import quote_plus
from collections import defaultdict
import ast
import json

def search(query):
    with urlopen('http://localhost:8983/solr/metamap/select?q={}&rows=200'.format(query)) as u:
        output_1 = json.loads(u.read().decode())
    post_num = []
    post_link = []
    for val in output_1['response']['docs']:
        post_num.append(val['PostNumber'][0])
        post_link.append(val['PostLink'][0])
    post_output = dict(zip(post_link, post_num))

    keywords_list = get_keywords(post_num)
    posts_list = comments(post_link, post_output)
    formatted_posts_list = formatPosts(posts_list)

    main_dict = {
        'total':len(posts_list),
        'posts':formatted_posts_list,
        'keyword':keywords_list
    }
    return main_dict

def formatPosts(postsObj):
    l1 = []
    for i in range(len(postsObj)):
        newMap = {}
        newMap["url"] = postsObj[i][0]
        newMap['replies'] = postsObj[i][1][0]
        newMap['title'] = postsObj[i][1][1]
        newMap['content'] = postsObj[i][1][2]

        newMap['symptoms'] = postsObj[i][1][3]
        newMap['treatments'] = postsObj[i][1][4]
        newMap['drugs'] = postsObj[i][1][5]
        newMap['bodyparts'] = postsObj[i][1][6]
        l1.append(newMap)

    return l1

def get_keywords(post_num):
    unique_num = list(set(post_num))
    symptoms = []
    treatments = []
    drugs = []
    bodyparts = []
    for num in unique_num:
        with urlopen('http://localhost:8983/solr/metamap/select?q=PostNumber%3A{}&rows=100'.format(num)) as u:
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

    keywords_dict = {}
    keywords_dict['symptoms'] = list(set(symptoms)) if symptoms else list()
    keywords_dict['treatments'] = list(set(treatments)) if treatments else list()
    keywords_dict['drugs'] = list(set(drugs)) if drugs else list()
    keywords_dict['bodyparts'] = list(set(bodyparts)) if bodyparts else list()

    return keywords_dict


def comments(post_link, post_output):
    all_links = list(set(post_link))
    reply_dict = defaultdict(int)
    for link in all_links:
        with urlopen('http://localhost:8983/solr/scrappedData/select?q=url%3A%22{}%22&rows=100'.format(link)) as u: 
            output_3 = json.loads(u.read().decode())
        post_link = []
        for res in output_3['response']['docs']:
            title = res['title'][0]
            content = res['content'][0]
            replies = res['replies'][0]
            post_link = (res['url'][0])

            if post_link in post_output:
                post_num = post_output[post_link]
                post_keywords = get_keywords([post_num])
            else:
                post_keywords = {'symptoms': list(), 'treatments': list(), 'drugs': list(), 'bodyparts': list()}

            replies_list = ast.literal_eval(replies)
            replies_count = len(replies_list)
            reply_dict[post_link] = (replies_count, title, content, *post_keywords.values())

    sorted_urls = sorted(reply_dict.items(), key = lambda x:x[1][0], reverse = True)
    return sorted_urls

