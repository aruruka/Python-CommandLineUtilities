## file_transferer.py

```
Syntax:
python file_transferer.py <files_dir> <files> <remote_servers> <--mode allower|excluder>

Example:
python file_transferer.py /root/downloads/ ebf_file_list.txt remote_servers.txt --mode excluder
python file_transferer.py /root/downloads/ ebf_file_list.txt remote_servers.txt --mode allower
python file_transferer.py /etc/yum.repos.d/ files.txt remote_servers.txt --mode allower
python file_transferer.py /opt/mapr/hadoop/hadoop-3.3.5/etc/hadoop/ files.txt remote_servers.txt --mode allower
```
