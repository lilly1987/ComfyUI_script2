import os
import torch
import safetensors.torch
import pytorch_lightning
from safetensors.torch import save_file
import glob
import shutil
import tqdm
from torch import Tensor

wd = os.getcwd()
print("working directory is ", wd)

filePath = __file__
print("This script file path is ", filePath)

absFilePath = os.path.abspath(__file__)
print("This script absolute path is ", absFilePath)

path, filename = os.path.split(absFilePath)
print("Script file path is {}, filename is {}".format(path, filename))

    
for (path, dir, files) in os.walk("..\\..\\models\\checkpoints"):
    for f in files:

        f = os.path.join(path, f)
        print(f)
        
        file_size = os.path.getsize(f) 
        print('File Size:', file_size, 'bytes')
        
        if (not f.lower().endswith(".safetensors")) and (not f.lower().endswith(".ckpt")):
            continue
            
        if "fp16" in f.lower():
            print(f'Skipping, as {f} already exists.')
            continue
        m=None
        if f.lower().endswith('.ckpt'):
            fn = f"{f.replace('.ckpt', '')}-fp16.safetensors"
            if fn in files:
                print(f'Skipping, as {fn} already exists.')
                shutil.move(f, f"{f}.bak")
                continue
            m = torch.load(f, map_location="cpu")

        if f.lower().endswith(".safetensors"):
            fn = f"{f.replace('.safetensors', '')}-fp16.safetensors"
            if fn in files:
                print(f'Skipping, as {fn} already exists.')
                shutil.move(f, f"{f}.bak")
                continue
            m = safetensors.torch.load_file(f, device="cpu")
            
        state_dict = m["state_dict"] if "state_dict" in m else m
            
        ok = {}
        
        for k, v in tqdm.tqdm(state_dict.items()):
            if "model_ema" not in k:

                if not isinstance(v, Tensor):
                    continue
                ok[k] = v.half()
                #print(f'v.dtype {v.dtype}.')
                #print(f'ok[k] {ok[k].dtype}.')
                #print(f'v.dtype==ok[k] {v.dtype==ok[k].dtype }.')
            
        safetensors.torch.save_file(ok, fn)
        print(f'Saved {fn}.')
        shutil.move(f, f"{f}.bak")

print('Done!')