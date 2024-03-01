import json

def updateLocalJson(filename: str = "testLevels.json"):
    global stages
    with open("testLevels.json") as file:
        stages = json.load(file)

def jsonRewrite(filename: str = "testLevels.json"):
    with open(filename, "w") as file:
        json.dump(stages, file, indent=4)