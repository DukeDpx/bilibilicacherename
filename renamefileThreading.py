# -*- coding: UTF-8 -*-
import os
import json
import shutil
import threading


newpath = ""
namestr = ""
pathstr = ""
nameindex = ""
beforesize = ""
threadlist = []


class myThread (threading.Thread):  # 继承父类threading.Thread
    def __init__(self, pathname,newname, newpath):
        threading.Thread.__init__(self)
        self.pathname = pathname
        self.newname = newname
        self.newpath = newpath

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        if not "mp4" in self.newname[1]:
            shutil.copyfile(self.pathname, self.newpath +
                            "\\"+self.newname[1]+".mp4")
            print(self.newname[1]+".mp4复制完成")
        else:
            shutil.copyfile(self.pathname, self.newpath +
                            "\\"+self.newname[1])
            print(self.newname[1]+"复制完成")

def scanfile(filepath, i):
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            i = i+1
            fileList = os.listdir(filepath)
            if i == 1:
                global beforesize
                beforesize = fileList.__len__()
                print("需复制文件共"+str(fileList.__len__())+"件")
            for chfile in fileList:
                if i == 1:
                    global nameindex
                    nameindex = chfile
                pathname = os.path.join(filepath, chfile)
                if os.path.isdir(pathname):
                    scanfile(pathname, i)
                else:
                    global threadlist
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
                        if array[array.__len__()-1] == "blv":
                            pathname = os.path.join(filepath, chfile)
                            newname = namestr.split("/")
                            thread = myThread(pathname, newname,newpath)
                            threadlist.append(thread)
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
        if not os.path.exists(pathstr+"/"+parentname):
            os.mkdir(parentname)
        return os.path.abspath(parentname)

def startFunc():
    filepath = input("输入要重命名的文件")
    scanfile(filepath, 0)
    for thread in threadlist:
        thread.start()
    for thread in threadlist:
        thread.join()
    listsize = os.listdir(pathstr)
    if beforesize == threadlist.__len__():
        print("所有文件复制完成")
    exit()

startFunc()
