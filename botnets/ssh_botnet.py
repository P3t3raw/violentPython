import pexpect

PROMPT = [r'# ', r'>>> ', r'> ', r'\$ ']

def send_command(child, cmd):
    """Send a command to the remote shell and print the output."""
    child.sendline(cmd)
    child.expect(PROMPT)
    output = child.before.decode(errors="ignore")
    print(output)

def connect(user, host, password, port=22):
    """Try to establish SSH connection using pexpect. Returns child on success, None on failure."""
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = f'ssh -p {port} {user}@{host}'
    try:
        child = pexpect.spawn(connStr, timeout=5)
        ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
        if ret == 0:
            print(f"[-] Error Connecting to {host}:{port} (timeout)")
            return None
        if ret == 1:
            child.sendline('yes')
            ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
            if ret == 0:
                print(f"[-] Error Connecting to {host}:{port} (key exchange timeout)")
                return None
        child.sendline(password)
        child.expect(PROMPT)
        return child
    except Exception as e:
        print(f"[-] Connection to {host}:{port} failed: {e}")
        return None

def botnet_command(targets, user, password, command):
    """Run a command across multiple SSH hosts."""
    for target in targets:
        host, port = parse_target(target)
        print(f"\n[+] Connecting to {host}:{port}...")
        child = connect(user, host, password, port)
        if child:
            print(f"[+] Running command on {host}:{port}: {command}")
            send_command(child, command)
            child.close()
        else:
            print(f"[-] Skipping {host}:{port}, could not connect.")

def interactive_shell(user, host, password, port=22):
    """Drop into a live SSH shell with a single host."""
    child = connect(user, host, password, port)
    if child:
        print(f"[+] Connected to {host}:{port}. Type your commands below.")
        print("    Type 'exit' or Ctrl-D to quit.\n")
        child.interact()   # Hand control over to user
    else:
        print(f"[-] Could not connect to {host}:{port}.")

def parse_target(target):
    """Parse host:port string into host and int(port). Defaults to port 22."""
    if ":" in target:
        host, port = target.split(":")
        return host, int(port)
    return target, 22

def main():
    # Example targets (default port 22 unless specified)
    targets = [
        # "localhost",
        "bandit.labs.overthewire.org:2220",
        "192.168.1.102"
    ]

    user = "bandit0"
    password = "bandit0"

    print("=== SSH Botnet Tool ===")
    print("1) Run batch command on all hosts")
    print("2) Drop into interactive shell with one host")
    choice = input("Select option (1/2): ").strip()

    if choice == "1":
        command = input("Enter command to run on all hosts: ")
        botnet_command(targets, user, password, command)
    elif choice == "2":
        for i, target in enumerate(targets, start=1):
            print(f"{i}) {target}")
        idx = int(input("Select host: ")) - 1
        if 0 <= idx < len(targets):
            host, port = parse_target(targets[idx])
            interactive_shell(user, host, password, port)
        else:
            print("Invalid selection.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
