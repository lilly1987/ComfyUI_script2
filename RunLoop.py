import os, sys, glob, json, random, time, copy
from urllib import request, parse

filename=os.path.splitext(os.path.basename(__file__))[0]
if __name__ == filename or __name__ =='__main__':
    from ConsoleColor import print, console
    from PromptMaker import *
    from JsonLoader import JsonLoader
    from ModelList import *
    from queue_prompt import *
else:
    from .ConsoleColor import print, console
    from .PromptMaker import *
    from .JsonLoader import JsonLoader
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
try:
    while True:
        
        JsonLoader(f"{settup['jsonpath']}settup.json",settup,True)
        JsonLoader(f"{settup['jsonpath']}chardic.json",chardic,True)
        JsonLoader(f"{settup['jsonpath']}charfill.json",charfill,True)
        JsonLoader(f"{settup['jsonpath']}ckptdic.json",ckptdic,True)
        JsonLoader(f"{settup['jsonpath']}loradic.json",loradic,True)
        JsonLoader(f"{settup['jsonpath']}vaedic.json",vaedic,True)
        
        #jsonget("styledic",styledic,True)
        if len(ckptdic) and random.random()<=settup["perckptdic"]:
            tmp=list(ckptdic.keys())
        else:
            tmp=ckptnames
        ckptname=random.choice(tmp)
        
        if len(vaedic) and random.random()<=settup["pervaedic"]:
            tmp=list(vaedic.keys())
        else:
            tmp=vaenames
        vaename=random.choice(tmp)
        
        if len(loradic) and random.random()<=settup["perloradic"]:
            tmp=list(loradic.keys())
        else:
            tmp=loranames
        loraname=random.choice(tmp)
        
        for ckptloopnum in range(0,settup["ckptloop"]):
            #console.rule(f" {ckptname} ckpt Loop {ckptloopnum+1} - {settup['ckptloop']} ")
            charnms = [list(chardic.keys())]
            char_name=random.choice(random.choice(charnms))
            for charloopnum in range(0,settup["charloop"]):
                # ----------------
                console.rule(f" {ckptname} - {char_name} - Loop - {charloopnum+1} / {settup['charloop']} - {ckptloopnum+1} / {settup['ckptloop']} " )
                #print(f"[{ccolor}]char_name : [/{ccolor}]",char_name)
                chard=copy.deepcopy(chardic[char_name])
                dset(chard,"ckpt_name",ckptname)
                dset(chard,"vae_name",vaename)
                #print(f"[{ccolor}]chard : [/{ccolor}]",chard)
                #print(f"[{ccolor}]charfill : [/{ccolor}]",charfill)
                for k in charfill:
                    #print(k)
                    if k in chard:
                        #print("charfill\[k]",charfill[k],True)
                        #print("chard\[k]",chard[k],True)
                        for k2 in charfill[k]:
                            #print("k2",k2,True)
                            #print("charfill\[k]\[k2]",charfill[k][k2],True)
                            if chard[k] is dict and not k2 in chard[k]:
                                chard[k][k2]=charfill[k][k2]
                    else:
                        #print(k,False)
                        chard[k]=charfill[k]
                # ----------------
                if len(loradic) and random.random()<=settup["perloradic"]:
                    tmp=list(loradic.keys())
                    loraname=random.choice(tmp)
                    dset(chard,"lora_add",{loraname:loradic[loraname]})
                else:
                    tmp=loranames
                    loraname=random.choice(tmp)
                    dset(chard,"lora_add",{loraname:""})
                #print("chard 1 : ",chard)
                #print("loradic[loraname] : ",loradic[loraname])
                # ----------------
                #print("chard 2 : ",chard)
                pm=PromptMaker(chard)
                
                prompt=pm.promptGet()
                print()
                print(f"[{ccolor}]prompt : [/{ccolor}]",prompt)
                
                queue_prompt(prompt)
                #quit()
except Exception:
    console.print_exception()
    quit()