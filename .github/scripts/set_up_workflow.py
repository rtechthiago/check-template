from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from pathlib import Path

def load_yaml(file_path):
    yaml = YAML()
    with open(file_path, 'r') as stream:
        return yaml.load(stream), yaml

def save_yaml(data, file_path, yaml):
    with open(file_path, 'w') as stream:
        yaml.dump(data, stream)

def replace_parameters_in_yaml(file_path, replacements):
    data, yaml = load_yaml(file_path)

    def recursive_replace(obj, replacements):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in replacements:
                    obj[key] = DoubleQuotedScalarString(replacements[key])
                elif isinstance(value, (dict, list)):
                    recursive_replace(value, replacements)
        elif isinstance(obj, list):
            for item in obj:
                recursive_replace(item, replacements)

    recursive_replace(data, replacements)
    save_yaml(data, file_path, yaml)
    print(f"Updated {file_path}")

def main():
    workflows_dir = Path(".github/workflows")
    replacements = {
        'bucket-name': "portal",
        'bucket-key': "portal",
        'node-version': "16"
    }

    for yaml_file in workflows_dir.glob("*.yml"):
        replace_parameters_in_yaml(yaml_file, replacements)

if __name__ == "__main__":
    main()
