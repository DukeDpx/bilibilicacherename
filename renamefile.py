# -*- coding: UTF-8 -*-
import os
import json
import shutil

newpath = ""
namestr = ""
pathstr = ""
nameindex = ""
beforesize=""

def scanfile(filepath, i):
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            i = i+1
            fileList = os.listdir(filepath)
            if i == 1:
                global beforesize
                beforesize=fileList.__len__()
                print("需复制文件共"+str(fileList.__len__())+"件")
            for chfile in fileList:
                if i == 1:
                    global nameindex
                    nameindex = chfile
                pathname = os.path.join(filepath, chfile)
                if os.path.isdir(pathname):
                    scanfile(pathname, i)
                else:
                    array = os.path.basename(chfile).split('.')
                    if os.path.basename(chfile) == "entry.json":
                        global newpath, namestr
                        pathname = os.path.join(filepath, chfile)
                        namestr = readjson(pathname, nameindex)
                        newpathname = os.path.join(
                            pathstr, namestr.split("/")[0])
                        if not os.path.exists(newpathname):
                            newpath = createdir(namestr)
                    if array.__len__() < 3:
                        if array[1] == "blv":
                            pathname = os.path.join(filepath, chfile)
                            newname = namestr.split("/")
                            if not "mp4" in newname[1]:
                                shutil.copyfile(pathname, newpath +
                                                "\\"+newname[1]+".mp4")
                                print(newname[1]+".mp4复制完成")
                            else:
                                shutil.copyfile(pathname, newpath +
                                                "\\"+newname[1])
                                print(newname[1]+"复制完成")
        else:
            if os.path.exists(filepath):
                array = os.path.basename(filepath).split('.')
                if array.__len__() < 3:
                    if array[1] == "blv":
                        newname = input("输入保存地址及保存文件名(eg:d:/aa/a.xx)")
                        shutil.copyfile(filepath, newname)
                        print(newname+"复制完成")

def readjson(jsonfile, nameindex):
    readfile = open(jsonfile, encoding='utf-8')
    entry = json.load(readfile)
    filepathtitle = entry['title']
    filename = nameindex + "-"+entry['page_data']['part']
    return filepathtitle+"/"+filename

def createdir(filename):
    global pathstr
    pathstr = input("输入文件导出地址")
    print("文件将导出到:"+pathstr)
    yorn = input("是否确认 y or n")
    if yorn == "y" or yorn == "":
        array = filename.split("/")
        parentname = array[0]
        childname = array[1]
        os.chdir(pathstr)
        os.mkdir(parentname)
        return os.path.abspath(parentname)

filepath = input("输入要重命名的文件")
scanfile(filepath, 0)
listsize=os.listdir(pathstr)
if beforesize==listsize.__len__():
    print("所有文件复制完成")
else:(
    print(str(listsize.__len__())+"文件复制完成")
)
yorn = input("是否还要继续复制？y or n")
if yorn == "y" or yorn == "":
    newfilepath = input("输入要重命名的文件")
    scanfile(newfilepath, 0)
else:
    exit()
