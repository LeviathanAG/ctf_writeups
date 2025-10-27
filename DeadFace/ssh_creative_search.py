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
        
        # Check more creative locations
        commands = [
            'cat /etc/profile\n',
            'cat ~/.profile 2>/dev/null\n',
            'cat ~/.bashrc 2>/dev/null\n',
            'cat /root/.bashrc 2>/dev/null\n',
            'history\n',
            'alias\n',
            'printenv | sort\n',
            'cat /proc/version\n',
            'uname -a\n',
            'id\n',
            'sudo -l 2>/dev/null\n',
            'find /usr -name "*hostbusters*" 2>/dev/null\n',
            'find /etc -name "*hostbusters*" 2>/dev/null\n',
            'grep -r "hostbusters3" / 2>/dev/null | head -5\n',
            'grep -r "deadface{hostbusters3" / 2>/dev/null\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(3)
            
            if channel.recv_ready():
                try:
                    output = channel.recv(32768).decode(errors='ignore')
                    print(output)
                except Exception as e:
                    print(f"[-] Error decoding: {e}")
        
        channel.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client.close()
        print("\n[*] Connection closed.")

if __name__ == "__main__":
    connect_and_get_flag()
