import glob
import json
import os

# GET MODULES
def getModules():
    return sorted([os.path.basename(f)[:-3] for f in glob.glob("userbot/modules/*.py") if os.path.isfile(f) and f.endswith(".py")])

# LOAD CONFIG FROM FILE
def loadConfig() -> dict:
    with open('config.json', encoding='UTF-8') as file:
        data = json.load(file)
    return data

# DUMP CONFIG IN FILE
def dumpConfig(config: dict) -> bool:
    with open('config.json', 'w+', encoding='UTF-8') as file:
        json.dump(config, file)
    return True

# RELOAD CONFIG
def reloadConfig(config: dict) -> dict:
    dumpConfig(config)
    return loadConfig()
