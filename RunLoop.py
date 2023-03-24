import os, sys, glob, json, random, time, copy
from urllib import request, parse

filename=os.path.splitext(os.path.basename(__file__))[0]
if __name__ == filename or __name__ =='__main__':
    from ConsoleColor import print, console
    from PromptMaker import *
    from JsonLoader import *
    from ModelList import *
    from queue_prompt import *
else:
    from .ConsoleColor import print, console
    from .PromptMaker import *
    from .JsonLoader import *
    from .ModelList import *
    from .queue_prompt import *

#----------------------


#----------------------
jsonpath=os.path.splitext(os.path.basename(__file__))[0]
settup={
    "ccolor" :"bright_yellow",
    "jsonpath": f"./{jsonpath}/",
    "ckptloop": 2,
    "charloop": 2,
    "perloradic": 0.5,
    "perckptdic": 0.5,
    "pervaedic" : 0.5,
}
#print("jsonpath : ",settup["jsonpath"],style="reset")
#----------------------
loradic={
    #"":""
}
#----------------------
ckptdic={
    #"":""
}
#----------------------
vaedic={
    #"":""
}
#----------------------
#styledic={
#    #"":""
#    #"arknightsChibiLora_v1" : "chibi, full body, "
#}
#----------------------------
chardic={
    #"SaegusaMayumi" : {
    #    "positive" : {
    #        "char" : "mayumi,__mayumi__,",
    #        "breasts" : "__breasts__,",
    #        "dress" : "{__SaegusaMayumidress__|__character_dress__|__dress_my__|},",
    #    },
    #    "negative" : {
    #        "1":"__no2d__",
    #        },
    #    "lora_name" : {
    #        "SaegusaMayumiTheIrregularAt_mayumi" : "",
    #        #"hunged_girl" : "__hunged_girl1__,"
    #        },
    #    "ckpt_name" : {},
    #    "vae_name" : {},
    #},
}
#----------------------------
charfill={
}
#----------------------------


#----------------------------
try:
    while True:
        
        JsonLoader(f"{settup['jsonpath']}settup.json",settup,True)
        
        #JsonLoader(f"{settup['jsonpath']}chardic.json",chardic,True)
        #JsonLoader(f"{settup['jsonpath']}charfill.json",charfill,True)
        #JsonLoader(f"{settup['jsonpath']}ckptdic.json",ckptdic,True)
        #JsonLoader(f"{settup['jsonpath']}loradic.json",loradic,True)
        #JsonLoader(f"{settup['jsonpath']}vaedic.json",vaedic,True)

        charlistdic=JsonLoader2(f"{settup['jsonpath']}char-*.json")
        filllistdic=JsonLoader2(f"{settup['jsonpath']}fill-*.json")
        ckptlistdic=JsonLoader2(f"{settup['jsonpath']}ckpt-*.json")
        vaelistdic=JsonLoader2(f"{settup['jsonpath']}vae-*.json")
        loralistdic=JsonLoader2(f"{settup['jsonpath']}lora-*.json")
        
        #jsonget("styledic",styledic,True)
        if len(ckptlistdic) and random.random()<=settup["perckptdic"]:
            tmp=list(random.choice(ckptlistdic).keys())
        else:
            tmp=ckptnames
        ckptname=random.choice(tmp)
        print(f"[{ccolor}]ckptname : [/{ccolor}]",ckptname)
        
        if len(vaelistdic) and random.random()<=settup["pervaedic"]:
            tmp=list(random.choice(vaelistdic).keys())
        else:
            tmp=vaenames
        vaename=random.choice(tmp)
        print(f"[{ccolor}]vaename : [/{ccolor}]",vaename)
        
        if len(loralistdic) and random.random()<=settup["perloradic"]:
            tmp=list(random.choice(loralistdic).keys())
        else:
            tmp=loranames
        loraname=random.choice(tmp)
        print(f"[{ccolor}]loraname : [/{ccolor}]",loraname)
        
        for ckptloopnum in range(0,settup["ckptloop"]):
            #console.rule(f" {ckptname} ckpt Loop {ckptloopnum+1} - {settup['ckptloop']} ")
            #charnms = [list(chardic.keys())]
            chardic=random.choice(charlistdic)
            char_name=random.choice(list(chardic.keys()))
            filldic=random.choice(filllistdic)

            
            for charloopnum in range(0,settup["charloop"]):
                # ----------------
                console.rule(f" {ckptname} - {char_name} - Loop - {charloopnum+1} / {settup['charloop']} - {ckptloopnum+1} / {settup['ckptloop']} " )
                #print(f"[{ccolor}]char_name : [/{ccolor}]",char_name)
                cchar=copy.deepcopy(chardic[char_name])
                cfilldic=copy.deepcopy(filldic)
                # ----------------
                #print(f"[{ccolor}]ccharfill : [/{ccolor}]",ccharfill)
                #print(f"[{ccolor}]cchar1 : [/{ccolor}]",cchar)
                for k in cfilldic:
                    #print(f"[{ccolor}]k : [/{ccolor}]",k)
                    if k in cchar:
                        #print(f"[{ccolor}]cchar\[k] : [/{ccolor}]",cchar[k])
                        for j in cfilldic[k]:
                            if j in cchar:
                                print(f"[{ccolor}]cfilldic\[{k}]\[{j}] : [/{ccolor}]",cfilldic[k][j])
                                print(f"[{ccolor}]cchar\[{k}]\[{j}] : [/{ccolor}]",cchar[k][j])
                            else:
                                cchar[k][j]=cfilldic[k][j]
                    else:
                        cchar[k]=cfilldic[k]
                #print(f"[{ccolor}]cchar2 : [/{ccolor}]",cchar)
                dset(cchar,"ckpt_name",ckptname)
                dset(cchar,"vae_name",vaename)
                # ----------------
                if len(loradic) and random.random()<=settup["perloradic"]:
                    tmp=random.choice(loradic)
                    tmp=list(tmp.keys())
                    loraname=random.choice(tmp)
                    dset(cchar,"lora_add",{loraname:tmp[loraname]})
                else:
                    tmp=loranames
                    loraname=random.choice(tmp)
                    dset(cchar,"lora_add",{loraname:""})
                # ----------------
                pm=PromptMaker(cchar)
                
                prompt=pm.promptGet()
                print()
                print(f"[{ccolor}]prompt : [/{ccolor}]",prompt)
                
                queue_prompt(prompt)
                #quit()
except Exception:
    console.print_exception()
    quit()