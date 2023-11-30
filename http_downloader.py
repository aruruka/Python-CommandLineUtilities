import os
import sys
import requests

# from arepl_dump import dump

def download_file(url, local_dir):
    local_filename = os.path.join(local_dir, url.split('/')[-1])
    print(f"Starting download of {local_filename}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    downloaded_size += len(chunk)
                    f.write(chunk)
                    done = int(50 * downloaded_size / total_size)
                    sys.stdout.write("\r[{}{}]".format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        print(f"\n{local_filename} download succeed")
        return local_filename
    except Exception as e:
        print(f"Failed to download {local_filename}. Error: {e}")
        return None

def main(base_url, target_files, local_dir):
    with open(target_files, 'r') as f:
        for line in f:
            file_name = line.strip()
            url = os.path.join(base_url, file_name)
            download_file(url, local_dir)

if __name__ == "__main__":
    # dump(sys.argv)
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        # Provide your arguments here for debugging
        main('http://local.storage.hpelocaldomain/artifactory/list/some/releases/component/version/redhat', 'Mapr_Packages.txt', '/root/mapr-downloads/')
