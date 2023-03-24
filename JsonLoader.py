#JsonLoader
import sys
import json
import ast
import glob,os
import shutil, time
if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
	
def JsonLoader2(path):
    try:
        print("path : ",path,style="reset")
        listdic=[]
        filelist=glob.glob(path)
        for file in filelist:
            tmp=JsonLoad(file)
            if len(tmp)>0:
                listdic+=[tmp]
        return listdic
    except Exception:
        print("listdic : ",listdic,style="reset")
        console.print_exception()
        quit()
        
def JsonLoad(full):
    with open(full, 'r', encoding='utf-8') as file:
        text=""
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
            if not line.startswith("#"):
                text+=line+"\n"
        
        text=ast.literal_eval(text)
        text=json.dumps(text)
        tmp =json.loads(text)

        return tmp
                    
                    
def JsonLoader(full,dic,update):
    try:
        path=os.path.split(full)[0]
        if not os.path.exists(path):
            os.makedirs(path)
            
        #with open(f"./RandomLoop/chars-{time.strftime('_%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as file:
        if os.path.exists(full):
            #print("jsondic file : ",full,style="reset")

        #print("type(dic) : ",type(dic),style="reset")
        #print("dic : ",dic,style="reset")
            f=os.path.split(full)
            if not os.path.exists(f[0]+"/backup/"):
                os.makedirs(f[0]+"/backup/")
            shutil.move(full, f[0]+"/backup/"+f[1]+time.strftime('.%y%m%d_%H%M%S'))

        with open(full, 'w', encoding='utf-8') as file:
            json.dump(dic, file, sort_keys=False, indent=4)

        return path
    except Exception:
        print("full : ",full,style="reset")
        print("text : ",text,style="reset")
        console.print_exception()
        quit()