

from microterminal import send, var
import os

helptext='''\u001b[33mls\u001b[0m\n\rSYNTAX: ls\n\rDESCRN: list information about the files (the current directory by default)\n\r'''

def run(opt, args):
  if args==[]:
    args=["."]
  for kwd in args:
    sercdir="{path}/{dir}".format(path=var.tl_path, dir=kwd).replace("//", "/").replace("//", "/").replace("//", "/")
    send("\u001b[33m{sercdir}:\u001b[0m\n\r".format(sercdir=sercdir))
    for obj in os.listdir(sercdir):
      stat = os.stat("{sercdir}/{obj}".format(sercdir=sercdir, obj=obj))
      if stat[0]==32768:
        if obj[-3:]==".py":
          if ("a" in opt) or ("all" in opt):
            send("size={size}B type={type} lastmod={lastmod} \u001b[32;1m{file}\u001b[0m\n\r".format(size=stat[6], type="py", lastmod=stat[8], file=obj))
          else:
            send("\u001b[32;1m{file}\u001b[0m  ".format(file=obj))
        else:
          if ("a" in opt) or ("all" in opt):
            send("size={size}B type={type} lastmod={lastmod} {file}\n\r".format(size=stat[6], type="file", lastmod=stat[8], file=obj))
          else:
            send("{file}  ".format(file=obj))
      elif stat[0]==16384:
        if ("a" in opt) or ("all" in opt):
          send("size={size}B type={type} lastmod={lastmod} \u001b[34;1m{file}\u001b[0m\n\r".format(size=stat[6], type="dir", lastmod=stat[8], file=obj))
        else:
          send("\u001b[34;1m{file}\u001b[0m  ".format(file=obj))
      else:
        if ("a" in opt) or ("all" in opt):
          send("size={size}B type={type} lastmod={lastmod} \u001b[34;1m{file}\u001b[0m\n\r".format(size=stat[6], type=stat[0], lastmod=stat[8], file=obj))
    send("\n\r")


