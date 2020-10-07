import glob
import json
import os

# Get module list
def getModules():
    return sorted([os.path.basename(f)[:-3] for f in glob.glob("userbot/modules/*.py") if os.path.isfile(f) and f.endswith(".py")])

# Load config from config.json
def loadConfig() -> dict:
    with open('config.json', encoding='UTF-8') as file:
        data = json.load(file)
    return data

# Dump dict config in config.json
def dumpConfig(config: dict) -> bool:
    with open('config.json', 'w+', encoding='UTF-8') as file:
        json.dump(config, file)
    return True

# Dump and load config
def reloadConfig(config: dict) -> dict:
    dumpConfig(config)
    return loadConfig()
