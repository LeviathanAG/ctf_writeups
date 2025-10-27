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
        
        # Look for recon output and check scripts more thoroughly
        commands = [
            'find ~ -name "recon_*" 2>/dev/null\n',
            'find ~ -name "techfinger_*" 2>/dev/null\n',
            'find ~ -name "*.txt" 2>/dev/null\n',
            'cat tools/subrecon.sh\n',
            'cat tools/techfinger.sh\n',
            'wc -c tools/subrecon.sh tools/techfinger.sh\n',
            'file tools/subrecon.sh tools/techfinger.sh\n',
            'head -1 tools/subrecon.sh | od -c\n',
            'head -1 tools/techfinger.sh | od -c\n',
        ]
        
        for cmd in commands:
            print(f"\n{'='*60}")
            print(f"[*] Executing: {cmd.strip()}")
            print('='*60)
            channel.send(cmd.encode())
            time.sleep(2)
            
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
