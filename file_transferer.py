#!/usr/bin/env python3

import os
import paramiko
import argparse

"""
FileTransferer is a class that is used to transfer files from one machine to a list of remote machines using paramiko.

AllowerFileTransferer is a subclass of FileTransferer that transfers files that are listed in a file from a source directory to a list of remote machines.

ExcluderFileTransferer is a subclass of FileTransferer that transfers files that are not listed in a file from a source directory to a list of remote machines.
"""


class FileTransferer:
    def __init__(self, files_dir, files, remote_servers):
        self.files_dir = files_dir
        self.files = self.read_file(files)
        self.remote_servers = self.read_file(remote_servers)

    def read_file(self, file_path):
        with open(file_path) as file:
            return set(line.strip() for line in file if line.strip())

    def transfer_file(self, server, source_file, file_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server)
        sftp = ssh.open_sftp()
        remote_path = os.path.join("/", file_path)
        remote_dir = os.path.dirname(remote_path)
        try:
            sftp.stat(remote_dir)
        except IOError:
            print(f"Creating {remote_dir} on {server}")
            ssh.exec_command(f"mkdir -p {remote_dir}")
        print(f"Transferring {source_file} to {server}:{remote_path}")
        sftp.put(source_file, remote_path)
        local_file_stat = sftp.stat(source_file)
        remote_file_stat = sftp.stat(remote_path)
        remote_file_stat.st_uid = local_file_stat.st_uid
        remote_file_stat.st_gid = local_file_stat.st_gid
        remote_file_stat.st_mode = local_file_stat.st_mode
        # sftp.chattr(remote_path, remote_file_stat)
        if local_file_stat.st_mode is not None:
            sftp.chmod(remote_path, local_file_stat.st_mode)
        sftp.close()
        ssh.close()


class AllowerFileTransferer(FileTransferer):
    def transfer(self):
        for root, dirs, files in os.walk(self.files_dir):
            for name in files:
                file_path = os.path.join(root, name)
                relative_path = os.path.relpath(file_path, self.files_dir)
                if relative_path not in self.files:
                    continue
                for server in self.remote_servers:
                    self.transfer_file(server, file_path, file_path)


class ExcluderFileTransferer(FileTransferer):
    def transfer(self):
        for root, dirs, files in os.walk(self.files_dir):
            for name in files:
                file_path = os.path.join(root, name)
                relative_path = os.path.relpath(file_path, self.files_dir)
                if relative_path in self.files:
                    continue
                for server in self.remote_servers:
                    self.transfer_file(server, file_path, file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files_dir", help="Directory path of files to be transferred")
    parser.add_argument(
        "files", help="Path of the file containing a list of files or folders"
    )
    parser.add_argument(
        "remote_servers", help="Path of the file containing a list of remote servers"
    )
    parser.add_argument(
        "--mode",
        default="allower",
        choices=["allower", "excluder"],
        help="Mode of operation: allower or excluder",
    )
    args = parser.parse_args()

    if args.mode == "allower":
        transferer = AllowerFileTransferer(
            args.files_dir, args.files, args.remote_servers
        )
    else:
        transferer = ExcluderFileTransferer(
            args.files_dir, args.files, args.remote_servers
        )

    transferer.transfer()


if __name__ == "__main__":
    main()
