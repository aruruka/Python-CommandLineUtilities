import paramiko
import paramiko.proxy

# User credentials
USER = "USERNAME"
PASSWORD = "PASSWORD"

# Remote directory
REMOTE_DIR = "/servdata/support/maprpatches/v7.2.0/rpm/"

# Files to download
FILES = [
    "20230817132658-md5sum.txt",
    "20230927003243-md5sum.txt",
    "CHANGELOG-7.2.0EBF.txt",
    "mapr-patch-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
    "mapr-patch-client-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
    "mapr-patch-loopbacknfs-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
    "mapr-patch-nfs4server-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
    "mapr-patch-posix-client-basic-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
    "mapr-patch-posix-client-platinum-7.2.0.5.20230927003243.GA-1.x86_64.rpm",
]

# Local directory
LOCAL_DIR = "/root/downloads/"

# Set up the proxy command
proxy_command = (
    "/usr/bin/ncat --proxy-type http --proxy PROXYSERVER.DOMAIN.DOMAIN.DOMAIN:8080 %s %d"
)

# Set up the SFTP client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Remote SFTP server
REMOTE_SFTP_SERVER = "SFTP.REMOTE.DOMAIN"
REMOTE_SFTP_PORT = 10000
# Connect to the remote server via the proxy
proxy = paramiko.proxy.ProxyCommand(proxy_command %
                                    (REMOTE_SFTP_SERVER, REMOTE_SFTP_PORT))
""" # Download the files
for file in FILES:
    sftp.get(REMOTE_DIR + file, LOCAL_DIR + file)

# Close the connection
sftp.close() """

client.connect(REMOTE_SFTP_SERVER,
               REMOTE_SFTP_PORT,
               username=USER,
               password=PASSWORD,
               sock=proxy)  # type: ignore

# Download the files
for file in FILES:
    sftp = client.open_sftp()
    remote_path = REMOTE_DIR + file
    local_path = LOCAL_DIR + file
    print(f"Downloading {remote_path} to {local_path}...")
    try:
        sftp.get(remote_path, local_path)
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")
    else:
        print(f"Download of {remote_path} to {local_path} complete.")
    finally:
        if sftp:
            sftp.close()

# Close the connection
if client:
    client.close()
