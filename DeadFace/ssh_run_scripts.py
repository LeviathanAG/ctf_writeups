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
        
        # Try to run the scripts and capture errors
        commands = [
            'sh -n tools/subrecon.sh 2>&1\n',
            'sh -n tools/techfinger.sh 2>&1\n',
            'sh tools/subrecon.sh 2>&1\n',
            'sh tools/techfinger.sh 2>&1\n',
            './tools/subrecon.sh 2>&1\n',
            './tools/techfinger.sh 2>&1\n',
            'cat tools/subrecon.sh | sh 2>&1 | head -10\n',
            'cat tools/techfinger.sh | sh 2>&1 | head -10\n',
            'hexdump -C tools/subrecon.sh | grep -A2 -B2 "deadface"\n',
            'hexdump -C tools/techfinger.sh | grep -A2 -B2 "deadface"\n',
            'od -c tools/subrecon.sh | grep -i dead\n',
            'od -c tools/techfinger.sh | grep -i dead\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(3)
            
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
