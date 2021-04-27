# CSE 546: Group 25
## Project - Mining Healthcare websites for COVID-19


### Steps of execution:
1) Start Apache solr by running the following 2 lines from the indexing/solr-8.8.2 folder \
```
    bin/solr start -c -p 8983 -s example/cloud/node1/solr \
    bin/solr start -c -p 7574 -s example/cloud/node2/solr -z localhost:9983
```
2) Run the API file present in the same folder using the following command: 
```
    python app.py
```
3) Run the UI from frontend/src folder
