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
        
        # Try to make scripts executable and run them
        commands = [
            'chmod +x tools/subrecon.sh tools/techfinger.sh\n',
            './tools/subrecon.sh example.com 2>&1\n',
            './tools/techfinger.sh /tmp/test.txt 2>&1\n',
            'which bash\n',
            '/bin/bash --version 2>&1\n',
            'ls -l /bin/ | grep bash\n',
            'cat tools/subrecon.sh | head -3\n',
            'sed -n "1,3p" tools/subrecon.sh\n',
            'sed -n "1,3p" tools/techfinger.sh\n',
            'cat tools/*.sh | grep -i flag\n',
            'cat tools/*.sh | grep "deadface"\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(2)
            
            if channel.recv_ready():
                try:
                    output = channel.recv(16384).decode(errors='ignore')
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
