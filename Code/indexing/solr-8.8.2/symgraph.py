import numpy as np
import csv, json

def getPostWiseKeywords(numPosts):

    allpostsKeywords = {}
    allKeywords = {}
    keywordsReverseMap = {}
    keyword_nameToId = {}
    keyword_idToName = {}
    keywordIndex = 0
    postIndex = 1

    with open('ontologies.csv') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        data = [r for r in reader]

        for row in data:
            postId = row[0]
            symptomId = row[1]
            symptomName = (row[2]).lower()
            treatmentId = row[3]
            treatmentName = (row[4]).lower()
            drugId = row[5]
            drugName = (row[6]).lower()
            bodypartId = row[7]
            bodypartName = (row[8]).lower()

            if symptomId == 'C1457887':
                continue

            if symptomId or treatmentId or drugId or bodypartId:
                if postId not in allpostsKeywords:
                    allpostsKeywords[postId] = {"index": postIndex, "keywordList": [], "keywordNames": []}
                    postIndex += 1

            if symptomId:
                if symptomId not in keyword_idToName:
                    keyword_idToName[symptomId] = symptomName
                if symptomName not in keyword_nameToId:
                    keyword_nameToId[symptomName] = symptomId

                allpostsKeywords[postId]["keywordList"].append(symptomId)
                allpostsKeywords[postId]["keywordNames"].append(symptomName)
                if symptomId not in allKeywords:
                    allKeywords[symptomId] = {"index": keywordIndex, "name": symptomName}
                    keywordsReverseMap[keywordIndex] = symptomId
                    keywordIndex += 1
                if numPosts != None and postIndex > numPosts:
                    break
                
            if treatmentId:
                if treatmentId not in keyword_idToName:
                    keyword_idToName[treatmentId] = treatmentName
                if treatmentName not in keyword_nameToId:
                    keyword_nameToId[treatmentName] = treatmentId

                allpostsKeywords[postId]["keywordList"].append(treatmentId)
                allpostsKeywords[postId]["keywordNames"].append(treatmentName)
                if treatmentId not in allKeywords:
                    allKeywords[treatmentId] = {"index": keywordIndex, "name": treatmentName}
                    keywordsReverseMap[keywordIndex] = treatmentId
                    keywordIndex += 1
                if numPosts != None and postIndex > numPosts:
                    break

            if drugId:
                if drugId not in keyword_idToName:
                    keyword_idToName[drugId] = drugName
                if drugName not in keyword_nameToId:
                    keyword_nameToId[drugName] = drugId

                allpostsKeywords[postId]["keywordList"].append(drugId)
                allpostsKeywords[postId]["keywordNames"].append(drugName)
                if drugId not in allKeywords:
                    allKeywords[drugId] = {"index": keywordIndex, "name": drugName}
                    keywordsReverseMap[keywordIndex] = drugId
                    keywordIndex += 1
                if numPosts != None and postIndex > numPosts:
                    break

            if bodypartId:
                if bodypartId not in keyword_idToName:
                    keyword_idToName[bodypartId] = bodypartName
                if bodypartName not in keyword_nameToId:
                    keyword_nameToId[bodypartName] = bodypartId

                allpostsKeywords[postId]["keywordList"].append(bodypartId)
                allpostsKeywords[postId]["keywordNames"].append(bodypartName)
                if bodypartId not in allKeywords:
                    allKeywords[bodypartId] = {"index": keywordIndex, "name": bodypartName}
                    keywordsReverseMap[keywordIndex] = bodypartId
                    keywordIndex += 1
                if numPosts != None and postIndex > numPosts:
                    break

    name_file = open("keyword_name.json", "w")
    json.dump(keyword_nameToId, name_file)
    name_file.close()
    id_file = open("keyword_id.json", "w")
    json.dump(keyword_idToName, id_file)
    id_file.close()
    
    return allpostsKeywords, allKeywords, keywordsReverseMap


def postWiseKeywordMatrix(allpostsKeywords, allKeywords):
    postKeywordsMat = []
    for postId, postInfo in allpostsKeywords.items():
        symptoms = [0 for x in range(len(allKeywords))]
        for symptomId in postInfo["keywordList"]:
            keywordMatIndex = allKeywords[symptomId]["index"]
            symptoms[keywordMatIndex] += 1
        postKeywordsMat.append(symptoms)
        print(postId, postInfo)
    return postKeywordsMat

def createSympGraph(postKeywordsMat, allKeywords):
    postKeywordsMat = np.array(postKeywordsMat)
    keywordGraphShape = (len(allKeywords),len(allKeywords))
    keywordGraph = np.zeros(keywordGraphShape)

    for postKeywords in postKeywordsMat:
        postKeywords = np.matrix(postKeywords)
        postkeywordGraph = np.matmul(postKeywords.transpose(), postKeywords)
        keywordGraph += postkeywordGraph

    print(keywordGraph.shape)
    return keywordGraph

def getSymgraphEdges(keywordGraph, keywordsReverseMap):
    keywordGraphList = keywordGraph.tolist()
    edgeList = []
    for row, symtoms in enumerate(keywordGraphList):
        for col in range(row + 1 ,len(keywordGraphList)):
            source = keywordsReverseMap[row]
            dest = keywordsReverseMap[col]
            weight = keywordGraphList[row][col]
            if weight >= 1:
                edgeList.append([source, dest, weight])
    return edgeList

def saveGraph(edgeList):
    with open('sympgraph.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["Source", "Destination", "Weight"])
        writer.writerows(edgeList)
        writeFile.close()

if __name__ == '__main__':
    allpostsKeywords, allKeywords, keywordsReverseMap = getPostWiseKeywords(None)
    postKeywordsMat = postWiseKeywordMatrix(allpostsKeywords, allKeywords)
    keywordGraph = createSympGraph(postKeywordsMat, allKeywords)
    edgeList = getSymgraphEdges(keywordGraph, keywordsReverseMap)
    saveGraph(edgeList)
