import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy()
)  # This is to add the server's SSH key automatically. Be aware that this can be a security risk

ssh.connect(
    "nebula.sabanciuniv.edu",
    username="emirkantul@sabanciuniv.edu",
    password="emirkantul",
)

stdin, stdout, stderr = ssh.exec_command("ls")

for line in stdout:
    print(line.strip("\n"))

ssh.close()
