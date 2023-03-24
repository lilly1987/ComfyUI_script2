# valuelib
import os, sys, glob, json, random, time, copy

if __name__ == os.path.splitext(os.path.basename(__file__))[0] or __name__ =='__main__':
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
    
def vchoice(v,t=None,inputkey=False):
    r=t
    if type(v) is list:
        if len(v)>0:
            r=random.choice(v) 
            r=vchoice(r,t,inputkey)
    if type(v) is dict:
        if len(v)>0:
            if inputkey:
                r=random.choice(list(v.keys()))
            else:
                r=v[random.choice(list(v.keys()))]
                r=vchoice(r,t,inputkey)

    #print("vchoice r : ", r)
    return r

def dget(d,k,t=None):
    r=d[k] if k in d else t
    return r

def dset(d,k,v):
    if k in d:
        d[k].update(v)
    else:
        d[k]=v

def ds_ls_join(dic):
    return djoin(dic)
def djoin(dic):
    #print("djoin dic : ", dic)
    
    tmp=""
    if type(dic) is dict:
        keylist=list(dic.keys())
        if len(keylist)>0:
            random.shuffle(keylist)
            for k in keylist:
                if type(dic[k]) is list:
                    tmp+=random.choice(dic[k])
                elif type(dic[k]) is str:
                    tmp+=dic[k]
    elif type(dic) is str:
        tmp=dic
    #print("djoin return : ", tmp)
    return tmp
    
def ljoin(list):
    #print("ljoin list : ", dic)

    tmp=""
    if len(list)>0:
        random.shuffle(list)
        for k in list:
            tmp+=k

    #print("ljoin return : ", tmp)
    return tmp
    
def listf(inputs,func,inputkey=True):
    if type(inputs) is dict: 
        keylist=list(inputs.keys())
        random.shuffle(keylist)
        if inputkey:
            tlst=[]
            for key in keylist:
                func(key)
                tlst+=[inputs[key]]
            return tlst
        else:
            for key in keylist:
                func(inputs[key])
    elif type(inputs) is list:
        random.shuffle(inputs)
        for input in inputs:
            func(input)
    elif type(inputs) is str:
        func(input)