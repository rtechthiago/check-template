import os
from pathlib import Path
import shutil

def compare_and_copy_files(local_dir, remote_dir, exclude_file=None):
    for root, _, files in os.walk(remote_dir):
        for file in files:
            remote_file = Path(root) / file
            local_file = Path(local_dir) / remote_file.relative_to(remote_dir)

            # Ignorar arquivos que precisam ser excluídos
            if exclude_file and remote_file.name == exclude_file:
                continue

            # Se o arquivo remoto não existir localmente, copiá-lo
            if not local_file.exists():
                print(f"File {local_file} does not exist locally. Copying from remote...")
                copy_file(remote_file, local_file)

def copy_file(remote_file, local_file):
    os.makedirs(local_file.parent, exist_ok=True)
    shutil.copy2(remote_file, local_file)
    print(f"Copied {remote_file} to {local_file}.")

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"  # Substitua pelo arquivo que deseja excluir

    compare_and_copy_files(local_dir, remote_dir, exclude_file)

if __name__ == "__main__":
    main()
