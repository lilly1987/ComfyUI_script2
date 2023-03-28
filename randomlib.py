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
    elif type(v) is dict:
        if len(v)>0:
            if inputkey:
                r=random.choice(list(v.keys()))
            else:
                r=v[random.choice(list(v.keys()))]
                r=vchoice(r,t,inputkey)
    elif type(v) is str:
        r=v
    return r

def lget(l,inputkey=False):
    if type(l) is dict:
        k=random.choice(list(l.keys()))
        if inputkey:
            r=k
        else:
            r=l[k]
    if type(l) is list:
        r=random.choice(l)
    elif type(l) is str:
        r=l
    return r

def dget(d,k,t=None):
    r=d[k] if k in d else t
    return r

def dset(d,k,v,strtodic=False):
    #try:
        if k in d:
            if type(d[k]) is str:
                d[k]={d[k]:d[k]}
            else:
                d[k].update(v)
        else:
            d[k]=v
    #except Exception:
    #    print("d : ",d,style="reset")
    #    print("v : ",v,style="reset")
    #    print("type d : ",type(d),style="reset")
    #    print("k : ",k,style="reset")
    #    print("type(d\[k])  : ",type(d[k]) ,style="reset")
    #    console.print_exception()
    #    quit()
        
def dupdate(d,k,v,strtodic=False):
    dset(d,k,v,strtodic)

def deepupdate(d1,d2):
    for k in d2:
        if k in d1:
            if type(d1[k]) is dict and type(d2[k]) is dict:
                deepupdate(d1[k],d2[k])
            elif type(d1[k]) is dict and type(d2[k]) is not dict:
                deepupdate(d1[k],{d2[k]:d2[k]})
            elif type(d1[k]) is not dict and type(d2[k]) is dict:
                d1[k]={d1[k]:d2[k]}
                deepupdate(d1[k],d2[k])
            elif type(d1[k]) is not dict and type(d2[k]) is not dict:
                d1[k]=d2[k]
        else:
            d1[k]=d2[k]

def deepfill(d1,d2):
    for k in d2:
        if k in d1:
            if type(d1[k]) is dict and type(d2[k]) is dict:
                deepfill(d1[k],d2[k])
            elif type(d1[k]) is dict and type(d2[k]) is not dict:
                deepupdate(d1[k],{d2[k]:d2[k]})
        else:
            d1[k]=d2[k]

def dadd(d,k,v):
    try:
        d[k]+=v
    except Exception:
        print("type d : ",type(d),style="reset")
        print("d : ",d,style="reset")
        console.print_exception()
        quit()

def ds_ls_join(dic):
    return djoin(dic)
def djoin(dic,shuffle=False):
    #print("djoin dic : ", dic)
    
    tmp=""
    if type(dic) is dict:
        keylist=list(dic.keys())
        if len(keylist)>0:
            if shuffle:
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
