from pymetamap import MetaMap
import pandas as pd
import json
from tqdm import tqdm

mm = MetaMap.get_instance('/home/ubuntu/public_mm/metamap20')
content = {'PostNumber':[],'SymptomId':[], 'SymptomName':[],'TreatmentId':[],'TreatmentName':[],'DrugId':[],'DrugName':[],'BodypartId':[],'BodypartName':[],'PostLink':[]}

with open('stage1_scrapping.json') as f:
    data = json.load(f)

for index,i in enumerate(tqdm(data)):
    temp = i
    con = []
    con.append(str(temp['content']))
    for i in temp['replies']:
        con.append(str(i['content']))
        if len(i['sub_replies']) != 0: 
            for j in i['sub_replies']:
                con.append(str(j))


    concepts,error = mm.extract_concepts(con,[k for k in range(1, (len(con)+1))])
    for concept in concepts:
        if len(concept._asdict()) == 10:
            
            if concept.semtypes == '[sosy]':
                content['PostLink'].append(temp['url'])
                content['SymptomId'].append(concept._asdict()['cui'])
                content['SymptomName'].append(concept._asdict()['preferred_name'])
                content['TreatmentId'].append('')
                content['TreatmentName'].append('')
                content['DrugId'].append('')
                content['DrugName'].append('')
                content['BodypartId'].append('')
                content['BodypartName'].append('')
                content['PostNumber'].append(index + 1)
            elif concept.semtypes == '[dsyn]':
                content['PostLink'].append(temp['url'])
                content['SymptomId'].append(concept._asdict()['cui'])
                content['SymptomName'].append(concept._asdict()['preferred_name'])
                content['TreatmentId'].append('')
                content['TreatmentName'].append('')
                content['DrugId'].append('')
                content['DrugName'].append('')
                content['BodypartId'].append('')
                content['BodypartName'].append('')
                content['PostNumber'].append(index + 1)
            elif concept.semtypes == '[topp]':
                content['PostLink'].append(temp['url'])
                content['SymptomId'].append('')
                content['SymptomName'].append('')
                content['TreatmentId'].append(concept._asdict()['cui'])
                content['TreatmentName'].append(concept._asdict()['preferred_name'])
                content['DrugId'].append('')
                content['DrugName'].append('')
                content['BodypartId'].append('')
                content['BodypartName'].append('')
                content['PostNumber'].append(index + 1)
            elif concept.semtypes == '[clnd]':
                content['PostLink'].append(temp['url'])
                content['SymptomId'].append('')
                content['SymptomName'].append('')
                content['TreatmentId'].append('')
                content['TreatmentName'].append('')
                content['DrugId'].append(concept._asdict()['cui'])
                content['DrugName'].append(concept._asdict()['preferred_name'])
                content['BodypartId'].append('')
                content['BodypartName'].append('')
                content['PostNumber'].append(index + 1)
            elif concept.semtypes == '[bpoc]':
                content['PostLink'].append(temp['url'])
                content['SymptomId'].append('')
                content['SymptomName'].append('')
                content['TreatmentId'].append('')
                content['TreatmentName'].append('')
                content['DrugId'].append('')
                content['DrugName'].append('')
                content['BodypartId'].append(concept._asdict()['cui'])
                content['BodypartName'].append(concept._asdict()['preferred_name'])
                content['PostNumber'].append(index + 1)

df = pd.DataFrame(content)
print(df)
df.to_csv('ontologies.csv', index = False)

