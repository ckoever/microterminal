
import usocket
import _thread
import time
import os

#write logfiles
debug = 0
#module variables
class var:
  mt_socket = False
  connection = False
  address = False
  imported = []
  tl_path="/"
  m_path=globals()["__path__"]
  
class builtin:
  def sendtl():
    raw = "\u001b[32;1m{user}@{controller}\u001b[0m: \u001b[34;1m{path}\u001b[0m$ "
    raw = raw.format(user="root", controller=os.uname()[0], path=var.tl_path)
    var.connection.send(raw)

#add log to logfile
def send(text):
  var.connection.send(text)

def addlog(text):
  if debug:
    log = open("{}/log.txt".format(globals()["__path__"]), "a")
    log.write("{timestamp} {text}\n".format(timestamp = time.localtime()[0:6] ,text=text))
    log.close()

#close connection (and socket)
def close(restart=True):
  try:
    var.connection.close()
  except Exception as ex:
    addlog("{type} {error}".format(type=type(ex), error=ex))
  if restart:
    #wait for terminal connection (eg. putty)
    var.connection, var.address = var.mt_socket.accept()
    #start session
    session()
  else:
    var.mt_socket.close()
    
  
def _start():
  #create microterminal-socket
  var.mt_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
  #bind to raw terminal

  var.mt_socket.bind(('', 9100))
  var.mt_socket.listen(True)
  addlog("socket created")
  #wait for terminal connection (eg. putty)
  var.connection, var.address = var.mt_socket.accept()
  addlog("connection from {adr}".format(adr=var.address))
  #--wait for connection--
  #start session
  session()
 
def start():
  _thread.start_new_thread(_start,[])
  
def format_request(request):
  #format request
  request=request.split()
  end = False
  command = request[0]
  args = []
  opt = []
  hargs = []
  for item in request[1:]:
    if item == "--":
      end = True
    elif (item[:2] == "--" and (not end)):
      hargs.append(item[2:])
    elif (item[:1] == "-" and (not end)):
      opt.append(item[1:])
    else:
      args.append(item)
  addlog("format_request -> command: {comm}; opt: {opt}; args: {args}; hargs: {hargs}".format(comm=command, opt=opt, args=args, hargs=hargs))
  return (command, opt, args, hargs)
    
def session():
  #start terminal session
  addlog("session -> session started with {adr}".format(adr=var.address))
  while True:
    try:
      builtin.sendtl()
    except:
      addlog("session -> close".format(adr=var.address))
      close()
    request = var.connection.recv(1024).decode()
    addlog("session -> got request {req}".format(req=request))
    
    if request.split():
      command, opt, args, hargs = format_request(request)
      
      modules = os.listdir(globals()["__path__"])
      modules.remove("__init__.py")   
      modules.remove("log.txt")

      if command in modules:
          if not(command in var.imported):
            exec("import {path}.{name} as mt_{name}".format(name=command, path=var.m_path.replace("/", ".")))
            var.imported.append(command)
          if "help" in hargs:
            send(eval("mt_{name}.helptext".format(name=command)))
          else:
            exec("{name}.run(opt={opt}, args={args})".format(name=command, opt=opt, args=args))
