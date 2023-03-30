# ModelList
import os, sys, glob, json, random, time, copy

if __name__ == os.path.splitext(os.path.basename(__file__))[0] or __name__ =='__main__':
    from ConsoleColor import print, console
    
else:
    from .ConsoleColor import print, console
    

#----------------------
ckptspath=os.path.join( 
    os.path.dirname(__file__),
    "..\\..\\models\\checkpoints\\*.safetensors"
)    
ckptfullpaths=glob.glob(ckptspath)
ckptnames=[os.path.basename(ckptfullpath) for ckptfullpath in ckptfullpaths]

if len(ckptnames) ==0 :
    console.rule(f"!!! ckpts file count 0 !!!")
    quit()
#----------------------
loraspath=os.path.join( 
    os.path.dirname(__file__),
    "..\\..\\models\\loras\\*.safetensors"
)    
lorafullpaths=glob.glob(loraspath)
loranames=[os.path.basename(lorafullpath) for lorafullpath in lorafullpaths]

#----------------------
vaespath=os.path.join( 
    os.path.dirname(__file__),
    "..\\..\\models\\VAE\\*.safetensors"
)    
vaefullpaths=glob.glob(vaespath)
vaenames=[os.path.basename(vaefullpath) for vaefullpath in vaefullpaths]

#print(ModelList)
print("ModelList")

ckptname=random.choice(ckptnames)
print(f"[cyan]ckpts cnt : [/cyan]{len(ckptnames)}")
loraname=random.choice(loranames)
print(f"[cyan]loras cnt : [/cyan]{len(loranames)}")
vaename=random.choice(vaenames)
print(f"[cyan]vaes cnt : [/cyan]{len(vaenames)}")
