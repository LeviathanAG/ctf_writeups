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
        
        # Check for hostbusters3 and 5, plus read the binary file
        commands = [
            'strings /home/mirveal/hostbusters6.bin\n',
            'xxd /home/mirveal/hostbusters6.bin | head -20\n',
            'cat /home/mirveal/.keys/public.pem\n',
            'find / -name "*hostbusters3*" 2>/dev/null\n',
            'find / -name "*hostbusters5*" 2>/dev/null\n',
            'find / -type f 2>/dev/null | grep -i hostbuster\n',
            'ls -la /var/log 2>/dev/null\n',
            'ls -la /opt 2>/dev/null\n',
            'ls -la /usr/local 2>/dev/null\n',
            'cat /etc/motd 2>/dev/null\n',
            'cat /etc/issue 2>/dev/null\n',
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
