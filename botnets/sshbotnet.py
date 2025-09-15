import pexpect

# Common shell prompts to expect after commands
PROMPT = [r'# ', r'>>> ', r'> ', r'\$ ']

def send_command(child, cmd):
    """Send a command to the remote shell and print the output."""
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before.decode(errors="ignore"))  # decode bytes to str

def connect(user, host, password):
    """Establish SSH connection using pexpect."""
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = f'ssh {user}@{host}'
    child = pexpect.spawn(connStr)

    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error Connecting (timeout)')
        return None
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('[-] Error Connecting (timeout after new key)')
            return None

    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = 'localhost'
    user = 'root'
    password = 'toor'

    child = connect(user, host, password)
    if child:
        send_command(child, 'cat /etc/shadow | grep root')

if __name__ == '__main__':
    main()
