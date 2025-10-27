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
        
        # Check the scripts more carefully and look for errors/flags
        commands = [
            'cat tools/subrecon.sh | grep -i deadface\n',
            'cat tools/techfinger.sh | grep -i deadface\n',
            'grep -i "deadface" tools/*\n',
            'cat tools/subrecon.sh | tail -20\n',
            'cat tools/techfinger.sh | tail -20\n',
            'bash -n tools/subrecon.sh\n',
            'bash -n tools/techfinger.sh\n',
            'bash tools/subrecon.sh 2>&1\n',
            'bash tools/techfinger.sh 2>&1\n',
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
