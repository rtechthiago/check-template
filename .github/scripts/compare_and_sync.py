import os
from pathlib import Path
import difflib
import sys, shutil

def compare_and_sync_file_contents(local_dir, remote_dir, exclude_file, preserve_options):
    for root, _, files in os.walk(remote_dir):
        for file in files:
            remote_file = Path(root) / file
            local_file = Path(local_dir) / remote_file.relative_to(remote_dir)

            if local_file.name in exclude_file:
                continue

            if not local_file.exists():
                print(f"File {local_file} does not exist in the remote repository. Copying to local repository.")
                copy_file(remote_file, local_file)
            else:
                with open(local_file, 'r') as lf, open(remote_file, 'r') as rf:
                    local_content = lf.readlines()
                    remote_content = rf.readlines()

                    diff = list(difflib.unified_diff(local_content, remote_content, fromfile=str(local_file), tofile=str(remote_file)))

                    if diff:
                        print(f"Differences found in {local_file}. Synchronizing changes while preserving options...")
                        sync_files(local_file, local_content, remote_content, preserve_options)
                        print(f"Synced {local_file} with {remote_file}.")
                        sys.exit(1)
                    else:
                        print(f"{local_file} is already up to date with {remote_file}.")

def copy_file(remote_file, local_file):
    os.makedirs(local_file.parent, exist_ok=True)
    shutil.copy2(remote_file, local_file)
    print(f"Copied {remote_file} to {local_file}.")
    sys.exit(1)

def sync_files(local_file, local_content, remote_content, preserve_options):
    new_content = []
    preserve_dict = {}

    # Armazena as opções a serem preservadas
    for line in local_content:
        for option in preserve_options:
            if option in line:
                preserve_dict[option] = line

    # Substitui o conteúdo do arquivo local pelo conteúdo do arquivo remoto
    for line in remote_content:
        option_found = False
        for option in preserve_options:
            if option in line:
                if option in preserve_dict:
                    new_content.append(preserve_dict[option])  # Mantém a opção preservada
                else:
                    new_content.append(line)  # Adiciona a linha do remoto se não estiver no local
                option_found = True
                break
        if not option_found:
            new_content.append(line)

    # Garante que as opções preservadas que não estão no remoto sejam adicionadas
    for option, line in preserve_dict.items():
        if option not in ''.join(remote_content):
            new_content.append(line)

    with open(local_file, 'w') as lf:
        lf.writelines(new_content)

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"
    preserve_options = ["- bucket_name: 'vai'"]  # Substitua com as opções que deseja preservar
    
    compare_and_sync_file_contents(local_dir, remote_dir, exclude_file, preserve_options)

if __name__ == "__main__":
    main()
