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
        
        # Check other users and search for all hostbusters flags
        commands = [
            'ls -la /home\n',
            'ls -laR /home 2>/dev/null\n',
            'cat /home/mirveal/hostbusters6.bin 2>/dev/null\n',
            'find /home -name "*hostbusters*" 2>/dev/null\n',
            'find /home -type f -readable 2>/dev/null | head -20\n',
            'cat /home/*/hostbusters* 2>/dev/null\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(3)
            
            if channel.recv_ready():
                output = channel.recv(32768).decode()
                print(output)
        
        channel.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client.close()
        print("\n[*] Connection closed.")

if __name__ == "__main__":
    connect_and_get_flag()
