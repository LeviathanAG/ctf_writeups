import paramiko
import time

# Connection details
hostname = "hostbusters.deadface.io"
username = "gh0st404"
password = "ReadySetG0!"

def connect_and_get_flag():
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"[*] Connecting to {hostname}...")
        client.connect(hostname, username=username, password=password, timeout=10)
        print("[+] Connected successfully!")
        
        # Open an interactive shell
        channel = client.invoke_shell()
        time.sleep(1)
        
        # Clear the initial output
        if channel.recv_ready():
            initial = channel.recv(4096).decode()
        
        # Send commands to search for hostbusters3
        commands = [
            'cat tools/subrecon.sh\n',
            'cat tools/techfinger.sh\n',
            'cat .ash_history\n',
            'grep -r "hostbusters3" . 2>/dev/null\n',
            'grep -r "deadface{" . 2>/dev/null\n',
            'find . -type f -exec cat {} \\; 2>/dev/null | grep -i hostbusters\n',
            'env\n',
            'printenv\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(2)
            
            if channel.recv_ready():
                output = channel.recv(16384).decode()
                print(output)
        
        channel.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client.close()
        print("\n[*] Connection closed.")

if __name__ == "__main__":
    connect_and_get_flag()
