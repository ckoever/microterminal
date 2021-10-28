
from microterminal import var, send
import os

helptext='''\u001b[33mcd\u001b[0m\n\rSYNTAX: cd [DIR]\n\rDESCRN: change the directory\n\r'''

def run(opt, args):
  if args:
    arg=args[0]
    try:
      if os.stat("{tl_path}/{arg}".format(arg=arg, tl_path=var.tl_path))[0]==16384:
        if arg == "..":
          var.tl_path = var.tl_path.rpartition("/")[0]
          var.tl_path = var.tl_path.rpartition("/")[0]
          var.tl_path += "/"
        else:
          var.tl_path += "/{dir}/".format(dir=arg)
          var.tl_path = var.tl_path.replace("//", "/")
      else:
        warn = "\u001b[41;1mNot dir\u001b[0m\n\r"
        send(warn)
    except Exception as inst:
      send("\u001b[41;1m{type} {error}\u001b[0m\n\r".format(type=type(inst), error=inst))
  else:
    var.tl_path = "/"

