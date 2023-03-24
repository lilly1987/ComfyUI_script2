import os, glob, sys,json,random,copy,time,types
from urllib import request, parse
from rich.progress import Progress,Console

if __name__ == os.path.splitext(os.path.basename(__file__))[0] or __name__ =='__main__':
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console


def queue_prompt(prompt, max=1):
    try:
        with Progress() as progress:
            
            #progress.update(task, completed =60)
            while True:
                if progress.finished:
                    task = progress.add_task("waiting", total=60)
                req =  request.Request("http://127.0.0.1:8188/prompt")        
                response=request.urlopen(req) 
                
                html = response.read().decode("utf-8")
                
                ld=json.loads(html)
                
                cnt=ld['exec_info']['queue_remaining']
                
                if cnt <max:
                    progress.stop()
                    break
                    f+=0.1
                progress.update(task, advance=1)

                time.sleep(1)
                
            p = {"prompt": prompt}
            data = json.dumps(p).encode('utf-8')
            req =  request.Request("http://127.0.0.1:8188/prompt", data=data)

        request.urlopen(req)
        print(f"send" )
    except Exception as e:     
        console.print_exception()

    time.sleep(2)
