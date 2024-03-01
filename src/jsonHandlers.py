import json

def updateLocalJson(filename: str = "levels.json"):
    global stages
    with open(filename) as file:
        stages = json.load(file)

def jsonRewrite(filename: str = "levels.json"):
    with open(filename, "w") as file:
        json.dump(stages, file, indent=4)