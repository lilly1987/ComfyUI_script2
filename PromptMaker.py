import os, sys, glob, json, random, time, copy, string

filename=os.path.splitext(os.path.basename(__file__))[0]
if __name__ == filename or __name__ =='__main__':
    from ConsoleColor import print, console
    #import ModelList
    from ModelList import *
    from wildcards import wildcards
    from randomlib import *
else:
    from .ConsoleColor import print, console
    #import .ModelList
    from .ModelList import *
    from .wildcards import wildcards
    from .randomlib import *
    
#----------------------------
positive={

}
negative={

}
ccolor="bright_yellow"

#----------------------------



#----------------------------
class PromptMaker:
    
    #----------------------------
    def pget(self,name,input):
        return self.prompts[self.nodeNums[name]]["inputs"][input]
        
    def pset(self,name,input,value=None):

        #print("pset1 : ",name,input,value)
        if not type(self.prompts[self.nodeNums[name]]["inputs"][input]) is list :
            while type(value) is list:
                value=vchoice(value)
        self.prompts[self.nodeNums[name]]["inputs"][input] = value
        #print("pset2 : ",self.prompts)

    def padd(self, nodename,class_type,inputs,func=None):
        n=f"{len(self.nodeNums.keys())}"
        self.nodeNums[nodename]=n
        self.prompts[n]={
            "class_type":class_type,
            "inputs":inputs
        }
        #print("padd : ", nodename,class_type,n)
        self.nodefuncs[nodename]=func
        return n

    #----------------------------
    def LoraLoader(self,name):
        return [
        "LoraLoaderText",
        {
            "model" : [self.loraModelLast,0],
            "clip"  : [self.loraClipLast ,1],
            "lora_name": name,
            "strength_model": random.uniform(0.5,1.0),
            "strength_clip" : random.uniform(0.5,1.0),
        }]
        
    def lora_add(self, name):
        if not name in self.loraNods:            
            t=self.LoraLoader(name)
            self.padd(
                name,
                t[0],
                t[1]
            )
            
            self.loraModelLast=self.nodeNums[name]
            self.loraClipLast =self.nodeNums[name]
            self.lora_add_after()

            self.loraNods[name]=t[1]
        return self.loraNods[name]
        
    def lora_add_after(self):
        self.pset("KSampler"        , "model", [self.loraModelLast,0])
        self.pset("positive" , "clip" , [self.loraClipLast ,1])
        self.pset("negative" , "clip" , [self.loraClipLast ,1])
        
    def lora_set(self,key,value):

        self.pset(self.loratag[self.c['lora']],key,value)
            
    #----------------------------
    def dupdate(self,update):
        for k in update:
            #print(f"[{ccolor}]k : [/{ccolor}]",k)
            if k in self.char:
                #print(f"if k in self.char", k,   k in self.char)
                #print(f"[{ccolor}]cfilldic\[{k}] : [/{ccolor}]",cfilldic[k])
                #print(f"[{ccolor}]cchar\[{k}] : [/{ccolor}]",cchar[k])
                for j in update[k]:
                    #print(f"for j in update[k]", j, type(self.char[k]))
                    if j in self.char[k]:
                         #print(f"j in self.char[k]", j in self.char[k],self.char[k])
                    #elif type(cchar[k]) is None:
                    #    cchar[k][j]=cfilldic[k][j]
                    #    print(f"[{ccolor}]cfilldic\[{k}]\[{j}] : [/{ccolor}]",cfilldic[k][j])
                    #    print(f"[{ccolor}]cchar\[{k}]\[{j}] : [/{ccolor}]",cchar[k][j])
                        continue
                    else:
                        #print(f"j in cchar[k]", j in self.char[k],self.char[k])
                        self.char[k][j]=update[k][j]
            else:
                #print(f"if k in self.char", k,   k in self.char)
                self.char[k]=update[k]
        if "lora_strength" in update :
            tmpu=update["lora_strength"]
            if "lora_strength" in self.char :
                tmpc=self.char["lora_strength"]
                for j in tmpu:
                    if not j in tmpc:
                        tmpc[j]=tmpu[j]
            else:
                self.char["lora_strength"]=update["lora_strength"]
            

    #----------------------------
    def promptGet(self):
        
        print("self.char" , self.char)
        
        positiveRandom=False
        if "positiveRandom" in self.char:
            positiveRandom=self.char["positiveRandom"]

        #--------------------------------
        if "batch_size" in self.char:
            self.pset("ImageSetup","batch_size",self.char["batch_size"])
        if "height" in self.char:
            self.pset("ImageSetup","height",self.char["height"])
        if "width" in self.char:
            self.pset("ImageSetup","width",self.char["width"])
            
        #--------------------------------
        if "denoise_min" in self.char and "denoise_max" in self.char:
            self.pset("KSampler","denoise",random.uniform(self.char["denoise_min"],self.char["denoise_max"]))
        #--------------------------------
        self.pset(
            "VAELoader",
            "vae_name", 
            vchoice(dget(self.char,"vae_name",vaenames),vaename)
        )
        #--------------------------------
        if "strength_model_min" in self.char and "strength_model_max" in self.char:
            for lora in self.loraNods:
                self.loraNods[lora]["strength_model"]=random.uniform(self.char["strength_model_min"],self.char["strength_model_max"])
        if "strength_clip_min" in self.char and "strength_clip_max" in self.char:        
            for lora in self.loraNods:                
                self.loraNods[lora]["strength_clip" ]=random.uniform(self.char["strength_clip_min" ],self.char["strength_clip_max" ])
        if "strength_model" in self.char:
            for lora in self.loraNods:
                self.loraNods[lora]["strength_model"]=self.char["strength_model"]
        if "strength_clip" in self.char:
            for lora in self.loraNods:
                self.loraNods[lora]["strength_clip"]=self.char["strength_clip"]
                
        #--------------------------------
        if "lora_name" in self.char:
            tmp=self.char["lora_name"]
            self.lora_add(vchoice(tmp))
        #--------------------------------
        inputs={}
        if "lora_set" in self.char:
            inputs=self.char["lora_set"]
        
        keys=list(inputs.keys())
        random.shuffle(keys)
        for key in keys:
            #print(f"[{ccolor}]key : [/{ccolor}]",key)
            lora=wildcards.run(key)
            self.lora_add(lora)
            tmp=inputs[key]
            if "strength_model_min" in tmp and "strength_model_max" in tmp: 
                self.pset(lora,"strength_model", random.uniform(tmp["strength_model_min"],tmp["strength_model_max"]))
                #self.loraNods[lora]["strength_model"]=random.uniform(tmp["strength_model_min"],tmp["strength_model_max"])
            if "strength_clip_min" in tmp and "strength_clip_max" in tmp: 
                self.pset(lora,"strength_clip",random.uniform(tmp["strength_clip_min" ],tmp["strength_clip_max" ]))
                #self.loraNods[lora]["strength_clip" ]=random.uniform(tmp["strength_clip_min" ],tmp["strength_clip_max" ])
            if "strength_model" in tmp : 
                self.pset(lora,"strength_model", tmp["strength_model" ])
                #self.loraNods[lora]["strength_model"]=tmp["strength_model" ]
            if "strength_clip" in tmp : 
                self.pset(lora,"strength_clip", tmp["strength_clip" ])
                #self.loraNods[lora]["strength_clip" ]=tmp["strength_clip" ]
                
            if "positive" in tmp : 
                dset(self.char,"positive",{lora:tmp["positive"]},True)
            if "negative" in tmp : 
                dset(self.char,"negative",{lora:tmp["negative"]},True)

                    
        #--------------------------------
        if "node_setup" in self.char:
            dicts=self.char["node_setup"]
            keys=dicts.keys()
            for key in keys:
                values=dicts[key]
                for v in values:
                    self.pset(key,v,values[v])

        #--------------------------------
        tmp=dget(self.char,"positive",positive)
        #print("tmp1" , tmp)
        tmp=djoin(tmp,positiveRandom) 
        #print("tmp2" , tmp)
        #print("[bright_yellow]positive : [/bright_yellow]", tmp)
        tmp=wildcards.run(tmp)
        print("[bright_yellow]positive : [/bright_yellow]", tmp)
        self.pset("positive","text", tmp)
        #--------------------------------
        tmp=djoin(dget(self.char,"negative",negative)) 
        tmp=wildcards.run(tmp)
        print("[bright_yellow]negative : [/bright_yellow]", tmp)
        self.pset("negative","text", tmp)
        #--------------------------------
        dset(self.char,"ckpt_name",ckptname)
        dset(self.char,"vae_name",vaename)
        #print(f"[{ccolor}]self.char1 : [/{ccolor}]",self.char)
        nm=dget(self.char,"ckpt_name",ckptnames)
        #print(f"[{ccolor}]nm : [/{ccolor}]",nm ,ckptname)
        nm=vchoice(nm,ckptname)
        #print(f"[{ccolor}]nm : [/{ccolor}]",nm)
        self.pset("CheckpointLoaderSimple","ckpt_name",nm)
        
        self.pset(
            "SaveImage",
            "filename_prefix",
            nm
            )

        #print(f"[{ccolor}]self.char : [/{ccolor}]",self.char)
        #--------------------------------
        print("self.char" , self.char)
        return self.prompts
        
    #----------------------------
    def __init__(self,char):
        #print(f"[{ccolor}]char : [/{ccolor}]",char)
        #self.char=copy.deepcopy(char)
        self.char=copy.deepcopy(char)
        
        self.prompts={}
        self.nodeNums={}
        self.nodefuncs={}
        self.loraNods={}
        
        self.padd(
            "CheckpointLoaderSimple",
            "CheckpointLoaderSimpleText",
            {
                "ckpt_name": ckptname
            }
        )

        self.loraModelLast=self.nodeNums["CheckpointLoaderSimple"]
        self.loraClipLast =self.nodeNums["CheckpointLoaderSimple"]

        self.padd(
            
            "positive",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": ""
            }
        )

        self.padd(
            
            "negative",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": ""
            }
        )

        self.padd(
            
            "ImageSetup",
            "EmptyLatentImage",
            {
                "batch_size": 1,
                "height": 512,
                "width": 512
            }
        )

        self.padd(
            
            "KSampler",
            "KSampler",
            {
                "model": [self.loraModelLast,0],
                "positive": [self.nodeNums["positive"],0],
                "negative": [self.nodeNums["negative"],0],
                "latent_image": [self.nodeNums["ImageSetup"],0],
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "seed": random.randint(0, 0xffffffffffffffff ),
                "steps": random.randint(20, 30 ),
                "cfg": 7,
                #"cfg": random.randint( int(4*2) , int(8*2) ) / 2,
                "denoise": 1 ,
                #"denoise": random.uniform(0.75,1.0) ,
            }
        )

        self.padd(
            
            "VAELoader",
            "VAELoader",
            {
                "vae_name": vaename
            }
        )

        self.padd(
            
            "VAEDecode",
            "VAEDecode",
            {
                "samples": [self.nodeNums["KSampler"],0],
                "vae": [self.nodeNums["VAELoader"],0],
            }
        )

        self.padd(
            
            "SaveImage",
            "SaveImageSimple",
            {
                "images": [self.nodeNums["VAEDecode"],0],
                "filename_prefix": os.path.splitext(
                    self.pget("CheckpointLoaderSimple","ckpt_name")
                )[0]
            }
        )
        