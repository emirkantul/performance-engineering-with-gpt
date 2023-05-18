import paramiko
import load_dotenv from dotenv
import os

load_dotenv()

SSH_HOST = os.getenv("SSH_HOST")
SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy()
)  # This is to add the server's SSH key automatically. Be aware that this can be a security risk

ssh.connect(
    SSH_HOST,
    username=SSH_USER,
    password=SSH_PASSWORD,
)

stdin, stdout, stderr = ssh.exec_command("ls")

for line in stdout:
    print(line.strip("\n"))

ssh.close()
