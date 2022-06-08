import json
import os
import re
from itertools import groupby

def createConfig(fileConfigName, config):
    if not os.path.exists(fileConfigName):
        with open(fileConfigName, 'w+') as f:
            f.write(config)
            f.close()
        return 1
    return 0

def loadConfig(fileConfigName, config):
    a = createConfig(fileConfigName, config)
    if not a:
        with open(fileConfigName) as f:
            arr = json.load(f)
            f.close()
        return arr
    return {"modid": "","exceptions": [],"lang": {}}

def registerConfig(fileConfigName, fileConfig, modid="", exception=""):
    config = loadConfig(fileConfigName, fileConfig)
    if not modid == "":
        config["modid"]=modid
    elif not exception == "":
        config["exceptions"].append(exception)
    with open(fileConfigName, "w") as f:
        f.write(json.dumps(config))
        f.close()

def testConfig(config):
    if config["modid"] == "" and config["exceptions"] == [] and config["lang"] == {}:
        return 1
    return 0

fileConfig = '{\n"modid": "",\n"exceptions": [],\n"lang": {}\n}'
configName = "./hmcft_config.json"
config = loadConfig(configName, fileConfig)

dirLangName = f'./src/main/recources/assets/{config["modid"]}'

dirItemTextureName = f'./src/main/resources/assets/{config["modid"]}/textures/items/'
dirItemModelName = f'./src/main/resources/assets/{config["modid"]}/models/item/'

def getItemModelFile(fileName): return '{\n"parent": "item/generated",\n"textures": {\n"layer0":"'+config["modid"]+':items/'+fileName+'"\n}\n}'

def getFilesFromDir(dirname):
    return os.listdir(dirname)

def isFile(name):
    arr = re.findall(r'(\w+).\w', name)
    return arr[0]

def dirItemsTextureLoader(dirName, config):
    files=getFilesFromDir(dirName)
    raw_arr=[]
    exceptions=config["exceptions"]
    for file in files:
        file_Name=isFile(file)
        if not file_Name in exceptions:
            raw_arr.append(file_Name)
    return [el for el, _ in groupby(raw_arr)]

def dirItemsModelLoader(dirName):
    files=getFilesFromDir(dirName)
    raw_arr=[]
    for file in files:
        file_Name=isFile(file)
        if not file_Name == "o":
            raw_arr.append(file_Name)
    return [el for el, _ in groupby(raw_arr)]

def createItemModelFile(fileName):
    with open(dirItemModelName+fileName+".json", "w+") as f:
        f.write(getItemModelFile(fileName))
        f.close()

def mainItems(dirItems, dirItem):
    arr_items=dirItemsTextureLoader(dirItems)
    arr_item=dirItemsModelLoader(dirItem)
    for item in arr_items:
        if not item in arr_item:
            createItemModelFile(item)
            print("Element ", item, " is aded!")

def mainLang(dirLangName): pass

def main():
    if testConfig(config):
        modid=input("put Modid:")
        registerConfig(configName, fileConfig, modid=modid)
        return 0

    print("Welcome to HMCfT!")
    print("1 - start create items model .json")
    print("2 - .lang add all models and items to lang file")
    print("3 - settings")
    print("4 - debug (Outputs an array of all files)")
    inp = input(":")
    if inp==1:
        mainItems(dirItemTextureName, dirItemModelName)
    elif inp=="2":
        pass
    elif inp=="3":
        print("Settings")
        print("1 - change modid")
        print("2 - add exception")
        inp_settings = input("Settings:")
        if inp_settings=="1":
            modid=input("Put modid:")
            registerConfig(configName, fileConfig, modid=modid)
        if inp_settings == "2":
            exception=input("Put exception:")
            registerConfig(configName, fileConfig, exception=exception)
    elif inp=="4":
        print("Array of item textures")
        print(dirItemsTextureLoader(dirItemTextureName, config))
        print("Array of item models")
        print(dirItemsModelLoader(dirItemModelName))
    else:
        print("There is no such option!")

main()

#createItemModelFile("test")
#print(dirItemsModelLoader(dirItemModelName))
#print(dirItemsTextureLoader(dirItemTextureName))