import optparse
from pexpect import pxssh


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before.decode(errors="ignore")


def botnet_command(command):
    for client in botNet:
        output = client.send_command(command)
        print(f'[*] Output from {client.host}')
        print(f'[+] {output}\n')


def add_client(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)


# === Main ===
botNet = []
add_client('10.10.10.110', 'root', 'toor')
add_client('10.10.10.120', 'root', 'toor')
add_client('127.0.0.1', 'kali', 'kali')

botnet_command('uname -v')
botnet_command('cat /etc/issue')
