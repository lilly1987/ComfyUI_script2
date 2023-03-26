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
jsonpath=os.path.splitext(os.path.basename(__file__))[0]
settup={
    "ccolor" :"bright_yellow",
    "jsonpath": f"./{jsonpath}/",

    "ckptloop": 6,
    "charloop": 2,

    "noloradic": 1.25, # ...
    "perloradic": 0.50,
    "perckptdic": 0.50,
    "pervaedic": 0.50,
	
	"positiveRandom" : False,
}

#print("jsonpath : ",settup["jsonpath"],style="reset")
#----------------------
loradic={
    "conceptCowgirl_v10": "__Cowgirl1__, cowgirl, sex, cowgirl position, {arms bound,| }",
    "gothGals_v10": "gothgal, wearing a gothgal outfit,"
}
#----------------------
ckptdic={
    random.choice(ckptnames): "detailed,",
    random.choice(ckptnames): "masterpiece,",
}
#----------------------
vaedic={
	random.choice(vaenames) : "detailed,",
	random.choice(vaenames) : "masterpiece,",
}
#----------------------------
chardic={
    "my": {
		"positive" : {
			"my": "__my__,",
		},
    },
    "your mind char name": {
		"positive": {
			"your mind tag": "blra blra",
			"quality": "{__quality__|__quality_my__|__quality1__},",
			"breasts": "__breasts__,",
			#"dress": "{__character_dress__|__dress_my__|__dress__|__dress_code__|__dress1__},",
			"skirt": "{__skirt__|},",
			"sleeve": "{__sleeve__|},",
			"acc": "{__acc_my__,|}",
			#"nsfw": "nsfw, (breastsout, breasts exposure, nipple exposure,{exposure,|}:1.2), {(sex:1.2)|}",
			"pregnant":"{(pregnant:1.2),|}",
			"body": "{slender, nature, curvy|__body__},",
			#"ear": "{|__ear__},",
			"off shoulder": "__shoulder__,",
			#"focus": "full body,",
			#"post": "{standing|sitting},",
			"abc":""
		},
		"negative": {
			"no":"__no2d__",
			"no34262" : "",
		} ,
		"lora_set" : {
			loraname : {     
				"strength_model_min": 0.5, 
				"strength_model_max": 0.750, 
				"strength_clip_min": 1.0,
				"strength_clip_max": 1.0,
				#"strength_model": 0.600,
				#"strength_clip" : 0.6000,
				"positive" : "lora prompt,",
			},		              
		},
    },
}

#----------------------------
filldic={
    "positive": {
        "quality": "{__quality__|__quality_my__|__quality1__},",
        "breasts": "__breasts__,",
        #"dress": "{__character_dress__|__dress_my__|__dress__|__dress_code__|__dress1__},",
        "skirt": "{__skirt__|},",
        "sleeve": "{__sleeve__|},",
        "acc": "{__acc_my__,|}",
        #"nsfw": "nsfw, (breastsout, breasts exposure, nipple exposure,{exposure,|}:1.2), {(sex:1.2)|}",
		"pregnant":"{(pregnant:1.2),|}",
        "body": "{slender, nature, curvy|__body__},",
        #"ear": "{|__ear__},",
        "off shoulder": "__shoulder__,",
        #"focus": "full body,",
        #"post": "{standing|sitting},",
    },
    "negative": "__no2d__",

	"lora_set": {
		loraname : {     
			"strength_model_min": 0.5, 
			"strength_model_max": 0.750, 
			"strength_clip_min": 1.0,
			"strength_clip_max": 1.0,
			#"strength_model": 0.600,
			#"strength_clip" : 0.6000,
			"positive" : "lora prompt,",
		},		
		#"animeTarotCardArtStyleLora_v30" : {     
		#	"strength_model_min": 0.5, 
		#	"strength_model_max": 0.750, 
		#	"strength_clip_min": 1.0,
		#	"strength_clip_max": 1.0,
		#	#"strength_model": 0.600,
		#	#"strength_clip" : 0.6000,
		#	"positive" : "hanfu,",
		#},		              
	},
	"node_setup":{
		"ImageSetup" : {
			"batch_size": 1,
			"height": 768,
			"width": 320,
		},
		"KSampler" : {
			"sampler_name": "dpmpp_sde",
			"scheduler": "karras",
		},
	},

	"denoise_min": 0.75,
	"denoise_max": 1.00,
	
	"strength_model_min": 0.75,
	"strength_model_max": 1.00,
	"strength_clip_min" : 0.75,
	"strength_clip_max" : 1.00,
}
#----------------------------
ckptloopnum=0
charloopnum=0
try:
    while True:
        
        settuplistdic=JsonLoader2(f"{settup['jsonpath']}settup.json",f"{settup['jsonpath']}settup.json",settup)

        print(f"[{ccolor}]settuplistdic : [/{ccolor}]",settuplistdic)
        print(f"[{ccolor}]settup : [/{ccolor}]",settup)
        if len(settuplistdic) :
            #key=random.choice(list(settuplistdic.keys()))
            #settup.update(settuplistdic[key])
            settup.update(settuplistdic[0])
        
        print(f"[{ccolor}]settup : [/{ccolor}]",settup)
        
        charlistdic=JsonLoader2(f"{settup['jsonpath']}char-*.json",f"{settup['jsonpath']}char-sample.json",chardic)
        filllistdic=JsonLoader2(f"{settup['jsonpath']}fill-*.json",f"{settup['jsonpath']}fill-sample.json",filldic)
        ckptlistdic=JsonLoader2(f"{settup['jsonpath']}ckpt-*.json",f"{settup['jsonpath']}ckpt-sample.json",ckptdic)
        vaelistdic=JsonLoader2(f"{settup['jsonpath']}vae-*.json",f"{settup['jsonpath']}vae-sample.json",vaedic)
        loralistdic=JsonLoader2(f"{settup['jsonpath']}lora-*.json",f"{settup['jsonpath']}lora-sample.json",loradic)
        
        if ckptloopnum <= 0:
            if len(ckptlistdic) and random.random()<=settup["perckptdic"]:
                tmp=list(random.choice(ckptlistdic).keys())
            else:
                tmp=ckptnames
            ckptname=random.choice(tmp)
            print(f"[{ccolor}]ckptname : [/{ccolor}]",ckptname)

            ckptloopnum = settup["ckptloop"]
        ckptloopnum-=1
        
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

        if charloopnum <= 0:
            chardic=random.choice(charlistdic)
            char_name=random.choice(list(chardic.keys()))
            charloopnum = settup["charloop"]
        charloopnum-=1
                # ----------------
        console.rule(f" {ckptname} - {ckptloopnum+1} / {settup['ckptloop']} " )
        console.rule(f" {char_name} - {charloopnum+1} / {settup['charloop']} " )
        #print(f"[{ccolor}]char_name : [/{ccolor}]",char_name)
        # ----------------
        filldic=random.choice(filllistdic)
        tmpdic={}
        tmpdic["ckpt_name"]=ckptname
        tmpdic["vae_name"]=vaename
        if len(loralistdic) and random.random()>=settup["noloradic"]:
            tmpdic["lora_set"]={loraname:""}
        #tmpdic.update(settup)
        #tmpdic.update(filldic)
        #print(f"[{ccolor}]tmpdic1 : [/{ccolor}]",tmpdic)
        deepupdate(tmpdic,chardic[char_name])
        #print(f"[{ccolor}]tmpdic2 : [/{ccolor}]",tmpdic)
        deepfill(tmpdic,filldic)
        #tmpdic.update(chardic[char_name])
        #print(f"[{ccolor}]tmpdic3 : [/{ccolor}]",tmpdic)

        # ----------------
        pm=PromptMaker(tmpdic)
        prompt=pm.promptGet()
        print()
        print(f"[{ccolor}]prompt : [/{ccolor}]",prompt)
        
        queue_prompt(prompt)
        #quit()
except Exception:
    console.print_exception()
    quit()