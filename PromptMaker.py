import os, sys, glob, json, random, time, copy

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
class PromptMaker:
    
    #----------------------------
    def pget(self,name,input):
        return self.prompts[self.nodeNums[name]]["inputs"][input]
        
    def pset(self,name,input,value):
        #print("pset : ",name,input)
        if not type(self.prompts[self.nodeNums[name]]["inputs"][input]) is list :
            while type(value) is list:
                value=vchoice(value)
        self.prompts[self.nodeNums[name]]["inputs"][input] = value
                
    def padd(self, nodename,class_type,inputs):
        n=f"{len(self.nodeNums.keys())}"
        self.nodeNums[nodename]=n
        self.prompts[n]={
            "class_type":class_type,
            "inputs":inputs
        }
        #print("padd : ", nodename,class_type,n)
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
        if not name in self.loraNums:            
            t=self.LoraLoader(name)
            self.padd(
                name,
                t[0],
                t[1]
            )
            
            self.loraModelLast=self.nodeNums[name]
            self.loraClipLast =self.nodeNums[name]
            self.lora_add_after()

            self.loraNums[name]=name
        return self.loraNums[name]
        
    def lora_add_after(self):
        self.pset("KSampler"        , "model", [self.loraModelLast,0])
        self.pset("CLIPTextEncodeN" , "clip" , [self.loraClipLast ,1])
        self.pset("CLIPTextEncodeP" , "clip" , [self.loraClipLast ,1])
        
    #----------------------------
    def promptGet(self):
    

        #--------------------------------        
        if "lora_name" in self.char:
        
            loras=self.char["lora_name"]
            print("lora_name" , loras)
            
            if type(loras) is dict:
                k=random.choice(list(loras.keys()))
                self.lora_add(k)
                if "positive" in self.char:
                    self.char["positive"].update(loras)
                else:
                    self.char["positive"]=loras

            elif type(loras) is list:
                self.lora_add(random.choice(loras))

            elif type(loras) is str:
                self.lora_add(loras)

        #--------------------------------        
        if "lora_add" in self.char:
            loras=self.char["lora_add"]
            print("type(loras)" , type(loras))
            print("loras" , loras)
            plst=listf(loras,self.lora_add,True)
            if plst:
                
                if "positive" in self.char:
                    tmp={}
                    
                    if type(loras) is dict:
                        tmp=loras
                    elif type(loras) is list:
                        tmp={string : "" for string in loras}
                    elif type(loras) is str:
                        tmp={loras:""}
                    self.char["positive"].update(tmp)
                else:
                    self.char["positive"]=loras
            print(" self.char\[positive]" ,  self.char["positive"])
        #--------------------------------
        tmp=dget(self.char,"positive",positive)
        print("tmp1" , tmp)
        tmp=djoin(tmp) 
        print("tmp2" , tmp)
        #print("[bright_yellow]positive : [/bright_yellow]", tmp)
        tmp=wildcards.run(tmp)
        print("[bright_yellow]positive : [/bright_yellow]", tmp)
        self.pset("CLIPTextEncodeP","text", tmp)
        #--------------------------------
        tmp=djoin(dget(self.char,"negative",negative)) 
        tmp=wildcards.run(tmp)
        print("[bright_yellow]negative : [/bright_yellow]", tmp)
        self.pset("CLIPTextEncodeN","text", tmp)
        #--------------------------------
        
        self.pset(
            "CheckpointLoaderSimple",
            "ckpt_name",
            vchoice(dget(self.char,"ckpt_name",ckptnames),ckptname)
            )

        #--------------------------------

        self.pset(
            "VAELoader",
            "vae_name", 
            vchoice(dget(self.char,"vae_name",vaenames),vaename)
        )

        
        #--------------------------------
        return self.prompts
        
    #----------------------------
    def __init__(self,char):
        print(f"[{ccolor}]char : [/{ccolor}]",char)
        #self.char=copy.deepcopy(char)
        self.char=char
        
        self.prompts={}
        self.nodeNums={}
        self.loraNums={}
        
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
            
            "CLIPTextEncodeP",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": ""
            }
        )

        self.padd(
            
            "CLIPTextEncodeN",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": ""
            }
        )

        self.padd(
            
            "EmptyLatentImage",
            "EmptyLatentImage",
            {
                "batch_size": 1,
                "height": 768,
                "width": 320
            }
        )

        self.padd(
            
            "KSampler",
            "KSampler",
            {
                "model": [self.loraModelLast,0],
                "positive": [self.nodeNums["CLIPTextEncodeP"],0],
                "negative": [self.nodeNums["CLIPTextEncodeN"],0],
                "latent_image": [self.nodeNums["EmptyLatentImage"],0],
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "seed": random.randint(0, 0xffffffffffffffff ),
                "steps": random.randint(20, 30 ),
                "cfg": random.randint( int(5*2) , int(9*2) ) / 2,
                "denoise": random.uniform(0.75,1.0) ,
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
        