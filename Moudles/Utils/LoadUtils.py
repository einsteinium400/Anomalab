import json
def loadItemFromJson(fileName):
    
  
    # Opening JSON file
    f = open(fileName)

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    itemList = list()
    itemList.append(data["rand"])
    itemList.append(data["lymphatics"])
    itemList.append(data["block of affere"])
    itemList.append(data["bl. of lymph. c"])
    itemList.append(data["bl. of lymph. s"])
    itemList.append(data["by pass"])
    itemList.append(data["extravasates"])
    itemList.append(data["regeneration of"])
    itemList.append(data["early uptake in"])
    itemList.append(data["lym.nodes dimin"])
    itemList.append(data["lym.nodes enlar"])
    itemList.append(data["changes in lym."])
    itemList.append(data["defect in node"])
    itemList.append(data["changes in node"])
    itemList.append(data["changes in stru"])
    itemList.append(data["special forms"])
    itemList.append(data["dislocation of"])
    itemList.append(data["exclusion of no"])
    itemList.append(data["no. of nodes in"])
    itemList.append(data["class"])
    return itemList
    