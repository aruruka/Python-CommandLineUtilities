import argparse
import pexpect

# Parse command line arguments
parser = argparse.ArgumentParser(description='Download files from SFTP server')
parser.add_argument('username', type=str, help='SFTP server username')
parser.add_argument('password', type=str, help='SFTP server password')
parser.add_argument('remote_dir', type=str, help='Remote directory to download from')
parser.add_argument('files', type=str, nargs='+', help='Files to download')
parser.add_argument('local_dir', type=str, help='Local directory to download to')
args = parser.parse_args()

# SFTP command to download files
sftp_command = f"sftp -o Port=10000 {args.username}@SFTP.REMOTE.DOMAIN:{args.remote_dir}/{{}} {args.local_dir}/"

# Create a new process for the SFTP command
sftp_process = pexpect.spawn(sftp_command.format(args.files[0]))

# Wait for the password prompt and enter the password
sftp_process.expect("password:")
sftp_process.sendline(args.password)

# Wait for the download to complete
sftp_process.expect(pexpect.EOF)

# Download the remaining files
for file in args.files[1:]:
    sftp_process = pexpect.spawn(sftp_command.format(file))
    sftp_process.expect("password:")
    sftp_process.sendline(args.password)
    sftp_process.expect(pexpect.EOF)

# Print a message indicating that the download is complete
print(f"Downloaded {len(args.files)} files to {args.local_dir}")