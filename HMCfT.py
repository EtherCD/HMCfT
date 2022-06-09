import json
import os
import re
from itertools import groupby


#Frequently used or forced functions
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

def saveConfig(fileConfigName, config):
    with open(fileConfigName, "w") as f:
        f.write(json.dumps(config))
        f.close()

def registerExceptionToConfig(fileConfigName, config, exception=""):
    if not exception in config["exceptions"]:
        config["exceptions"].append(exception)
        saveConfig(fileConfigName, config)
    else:
        print("The element is already in the array")

def updateConfig(fileConfigName, config, modid="", exception="", toException=""):
    if not modid == "":
        config["modid"]=modid
    if not exception == "":
        if exception in config["exceptions"]:
            if toException == "":
                config["exceptions"].remove(exception)
            else:
                config["exceptions"][config["exceptions"].index(exception)]=toException
    saveConfig(fileConfigName, config)

def testConfig(config_other):
    if config_other["modid"] == "" and config_other["exceptions"] == [] and config_other["lang"] == {}:
        return 1
    return 0

def getItemModelFile(fileName): return '{\n"parent": "item/generated",\n"textures": {\n"layer0":"'+config["modid"]+':items/'+fileName+'"\n}\n}'

def getFilesFromDir(dirname):
    return os.listdir(dirname)

def isFile(name):
    arr = re.findall(r'(\w+).\w', name)
    return arr[0]

def createItemModelFile(fileName):
    with open(dirItemModelName+fileName+".json", "w+") as f:
        f.write(getItemModelFile(fileName))
        f.close()

def openFile(dirName ,fileName):
    with open(dirName+fileName) as f:
        arr = f.read()
    return arr

def langFileLoader(dirLangName, FileName):
    lines = openFile(dirLangName, FileName)
    raw_arr = re.findall(r'item.(\w+).name=\w+', lines)
    #arr = re.findall(r'(\w+)', lines)
    #print(arr)
    #if arr != []:
    #    return raw_arr.extend(arr)
    return raw_arr

#Constan's
text_start="""Welcome to HMCfT!
1 - Start create items model .json
2 - .lang add all models and items to lang file
3 - Settings
4 - Debug (Outputs an array of all files)"""
text_settings="""Settings
1 - Change modid
2 - Add exception
3 - Change/Delate exception"""

fileConfig = '{\n"modid": "",\n"exceptions": [],\n"lang": {}\n}'
configName = "./hmcft_config.json"
config = loadConfig(configName, fileConfig)


dirLangName = f'./src/main/resources/assets/{config["modid"]}/lang/'

dirItemTextureName = f'./src/main/resources/assets/{config["modid"]}/textures/items/'
dirItemModelName = f'./src/main/resources/assets/{config["modid"]}/models/item/'

def dirItemsTextureLoader(dirName, config):
    files=getFilesFromDir(dirName)
    raw_arr=[]
    exceptions=config["exceptions"]
    for file in files:
        file_Name=isFile(file)
        if not file_Name in exceptions:
            raw_arr.append(file_Name)
    return [el for el, _ in groupby(raw_arr)]

def dirLangLoader(dirName):
    files=getFilesFromDir(dirName)
    raw_arr=[]
    for file in files:
        file_Name=isFile(file)
        if file_Name != "o":
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

def mainItems(dirItems, dirItem):
    arr_items=dirItemsTextureLoader(dirItems)
    arr_item=dirItemsModelLoader(dirItem)
    for item in arr_items:
        if not item in arr_item:
            createItemModelFile(item)
            print("Element ", item, " is aded!")
    print("Done!")

def langFileRegister(dirLangName, FileName, toWrite):
    with open(dirLangName+FileName, "r+") as f:
        f.seek(0, 2)
        f.write(toWrite)

def mainLang(dirLangName, dirItem): 
    lang_files_arr = dirLangLoader(dirLangName)
    c_name = lang_files_arr[0]+".lang"
    arr = langFileLoader(dirLangName, c_name)
    arr_item=dirItemsModelLoader(dirItem)
    other_arr = []
    for item in arr_item:
        if not item in arr:
            a = input(f"Put name for {item} (Or enter nothing):")
            if a != "":
                other_arr.append(f"item.{item}.name={a}")
    for lang_file in lang_files_arr:
        current_name = lang_file+".lang"
        for elem in other_arr:
            langFileRegister(dirLangName, current_name, "\n"+elem+"\n")
            print(f"Element '{elem}' is aded! In {lang_file}")
    print("Done")

def main():
    if testConfig(config):
        modid=input("put Modid:")
        updateConfig(configName, config, modid=modid)
        return 0
    exceptions = config["exceptions"]

    print(text_start)
    inp = input(":")
    if inp==1:
        mainItems(dirItemTextureName, dirItemModelName)
    elif inp=="2":
        mainLang(dirLangName, dirItemModelName)
    elif inp=="3":
        print(text_settings)
        inp_settings = input("Settings:")
        if inp_settings=="1":
            modid=input("Put modid:")
            updateConfig(configName, config, modid=modid)
        elif inp_settings == "2":
            exception=input("Put exception:")
            if exception in exceptions:
                print("The element is already in the array!")
            registerExceptionToConfig(configName, config, exception=exception)
        elif inp_settings == "3":
            print(exceptions)
            inp_exception=input("The name of the exception being changed:")
            if inp_exception in exceptions:
                inp_out=input(f"Put name for {inp_exception} (or nothing to delete):")
                updateConfig(configName, config, exception=inp_exception, toException=inp_out)
    elif inp=="4":
        print("Array of item textures")
        print(dirItemsTextureLoader(dirItemTextureName, config))
        print("Array of item models")
        print(dirItemsModelLoader(dirItemModelName))
    else:
        print("There is no such option!")

main() #Record in 200 lines!
#createItemModelFile("test")
#print(dirItemsModelLoader(dirItemModelName))
#print(dirItemsTextureLoader(dirItemTextureName))