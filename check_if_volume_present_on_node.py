import argparse
import re
import subprocess
import json
from datetime import datetime
from dateutil import tz
from collections import OrderedDict

# Add type hints to the parameter - node_ip_list and parameter - mapr_fs_port, their type is String.
def main(node_ip_list_str: str, mapr_fs_port_str: str):
    # Convert node_ip_list to a List of string.
    node_ip_list_list = node_ip_list_str.split(',')
    print(node_ip_list_list)
    
    # Convert variable mapr_fs_port to int. If the conversion fails, use default value 5660
    try:
        mapr_fs_port = int(mapr_fs_port_str)
    except ValueError:
        mapr_fs_port = 5660
    print(mapr_fs_port)
    
    target_fileservers = [f'{ip}:{mapr_fs_port}' for ip in node_ip_list_list]
    
    # Run the command and redirect the output to a file
    command = "sudo -E -u mapr maprcli volume list -output terse -columns volumename"
    print("Executing command: " + command + "\nAnd writing results to > Volumes.txt")
    with open("Volumes.txt", "w") as output_file:
        subprocess.run(command, shell=True, stdout=output_file)

    # Read the file
    with open("Volumes.txt", "r") as file:
        lines = file.readlines()

    # Remove the space and tab symbols at the beginning and end of each line
    lines = [line.strip() for line in lines]

    # Remove the first line
    lines = lines[1:]

    # Remove the lines matching the regular expression
    lines = [line for line in lines if not re.match(r'.*\.local\..*', line)]

    # Write the result back to the file
    with open("Volumes.txt", "w") as file:
        file.write('\n'.join(lines))
        
    # Read the file
    with open("Volumes.txt", "r") as file:
        volumes = [line.strip() for line in file]
        
    results = OrderedDict()
    status = 'NG'
    results_data = []
    for volume in volumes:
        volume_result = {volume: []}
        for target_fileserver in target_fileservers:
            command = f'sudo -E -u mapr maprcli dump volumenodes -volumename {volume} -json | grep {target_fileserver}'
            print("Executing command: " + command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = process.communicate()
            print(output.decode())
            if output:
                volume_result[volume].append({target_fileserver: "Yes"})
            else:
                volume_result[volume].append({target_fileserver: "No"})
        results_data.append(volume_result)
    # If volume_result not null, then results["status"] = "OK"
    if results_data:
        status = 'OK'

    # Get the current date and time
    current_datetime = datetime.now()
    # Get the current timestamp
    timestamp = current_datetime.timestamp()
    timestamp_int = int(timestamp)
    results["timestamp"] = timestamp_int
    # Convert to the local timezone
    local_tz = tz.tzlocal()
    current_datetime_local_tz = current_datetime.astimezone(local_tz)
    # Format the date and time
    formatted_datetime = current_datetime_local_tz.strftime("%Y-%m-%d %I:%M:%S.%f %Z%z %p")
    results["timeofday"] = formatted_datetime
    results["status"] = status
    results["total"] = len(results_data)
    results["data"] = results_data

    print("Writing results to file Check_IfVolumePresent_on_Node-Results.json")
    with open("Check_IfVolumePresent_on_Node-Results.json", "w") as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if a volume is present on a node.')
    parser.add_argument('--node_ip_list', type=str, required=True, help='List of node IPs')
    parser.add_argument('--mapr_fs_port', type=str, required=True, help='MapR FS port')
    args = parser.parse_args()
    # args = parser.parse_args(['--node_ip_list', '10.1.1.1,10.1.1.2', '--mapr_fs_port', '5660'])

    main(args.node_ip_list, args.mapr_fs_port)