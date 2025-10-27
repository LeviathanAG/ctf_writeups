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
        
        # List files in home directory
        print("\n[*] Listing files in home directory...")
        stdin, stdout, stderr = client.exec_command('ls -la ~', get_pty=True)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(output)
        if error:
            print(f"Error: {error}")
        
        # Check for common flag file names
        flag_commands = [
            'cat ~/flag.txt',
            'cat ~/flag',
            'cat ~/.flag',
            'cat ~/user.txt',
            'find ~ -name "*flag*" -type f 2>/dev/null',
            'find ~ -name "*.txt" -type f 2>/dev/null',
        ]
        
        for cmd in flag_commands:
            print(f"\n[*] Executing: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print(f"[+] Output:\n{output}")
            if error and "No such file" not in error:
                print(f"[-] Error: {error}")
        
        # Get current directory
        print("\n[*] Checking current directory...")
        stdin, stdout, stderr = client.exec_command('pwd', get_pty=True)
        print(f"Current directory: {stdout.read().decode().strip()}")
        
    except paramiko.AuthenticationException:
        print("[-] Authentication failed. Please check credentials.")
    except paramiko.SSHException as e:
        print(f"[-] SSH error: {e}")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client.close()
        print("\n[*] Connection closed.")

if __name__ == "__main__":
    connect_and_get_flag()
