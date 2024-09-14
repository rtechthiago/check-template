from ruamel.yaml import YAML
from pathlib import Path
import sys
import shutil

def load_yaml(file_path):
    yaml = YAML()
    with open(file_path, 'r') as stream:
        return yaml.load(stream), yaml

# def save_yaml(data, file_path, yaml):
#     with open(file_path, 'w') as stream:
#         yaml.dump(data, stream)

def compare_yaml(local_file, remote_file, fixed_keys):
    local_data, _ = load_yaml(local_file)
    remote_data, _ = load_yaml(remote_file)

    # Preserve fixed keys in local data
    for key in fixed_keys:
        if key in local_data and key.startswith("bucket"):
            remote_data[key] = local_data[key]

    return local_data != remote_data

# def sync_file(local_file, remote_file, yaml):
#     remote_data, _ = load_yaml(remote_file)
#     save_yaml(remote_data, local_file, yaml)

def compare_and_sync_directories(local_dir, remote_dir, fixed_keys):
    yaml = YAML()
    files_changed = False

    local_dir_path = Path(local_dir)
    remote_dir_path = Path(remote_dir)

    for remote_file in remote_dir_path.glob("**/*.yml"):
        relative_path = remote_file.relative_to(remote_dir_path)
        local_file = local_dir_path / relative_path

        if not local_file.exists():
            print(f"New file {relative_path} found in remote repository. Copying to local.")
            shutil.copy2(remote_file, local_file)
            files_changed = True
        else:
            if compare_yaml(local_file, remote_file, fixed_keys):
                print(f"Differences found in {relative_path}. Syncing changes.")
                shutil.copy2(remote_file, local_file)
                files_changed = True

    if files_changed:
        print("Differences were found and synchronized. Pipeline will be make push.")
    else:
        print("No differences found. Pipeline will continue.")

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    fixed_keys = ["bucket-name", "bucket-key", "node-version"]

    compare_and_sync_directories(local_dir, remote_dir, fixed_keys)

if __name__ == "__main__":
    main()
