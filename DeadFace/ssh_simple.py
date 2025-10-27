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
            print("[*] Initial output:")
            print(initial)
        
        # Send commands
        commands = [
            'ls -la\n',
            'cat flag.txt\n',
            'cat flag\n',
            'cat .flag\n',
            'cat user.txt\n',
            'find . -name "*flag*" 2>/dev/null\n',
            'find . -name "*.txt" 2>/dev/null\n',
            'cat $(find . -name "*flag*" 2>/dev/null | head -1)\n',
        ]
        
        for cmd in commands:
            print(f"\n[*] Executing: {cmd.strip()}")
            channel.send(cmd.encode())
            time.sleep(2)
            
            if channel.recv_ready():
                output = channel.recv(8192).decode()
                print(output)
        
        channel.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client.close()
        print("\n[*] Connection closed.")

if __name__ == "__main__":
    connect_and_get_flag()
