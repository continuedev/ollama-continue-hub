#!/usr/bin/env python3

import os
import logging
import argparse

DEFAULT_VERSION = "1.0.0"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the models and their capabilities
models = {
    "deepseek-r1": {
        "1.5b": ["chat", "edit", "apply", "autocomplete"],
        "7b": ["chat", "edit", "apply", "autocomplete"],
        "8b": ["chat", "edit", "apply", "autocomplete"],
        "14b": ["chat", "edit", "apply"],
        "32b": ["chat", "edit", "apply"]
    },
    "nomic-embed-text": {
        "latest": ["embed"]
    },
    "llama3.1": {
        "8b": ["chat", "edit", "apply"],
        "70b": ["chat", "edit", "apply"]
    },
    "llama3.2": {
        "1b": ["chat", "edit", "apply"],
        "3b": ["chat", "edit", "apply"]
    },
    "mistral": {
        "7b": ["chat", "edit", "apply"],
    },
    "qwen2.5-coder": {
        "1.5b": ["chat", "edit", "apply", "autocomplete"],
        "3b": ["chat", "edit", "apply", "autocomplete"],
        "7b": ["chat", "edit", "apply", "autocomplete"],
        "14b": ["chat", "edit", "apply"],
        "32b": ["chat", "edit", "apply"]
    },
}

def create_yaml_files(models, version):
    base_path = './blocks/public'

    # Create the directory if it doesn't exist
    try:
        os.makedirs(base_path)
    except FileExistsError:
        pass

    for model_name, model_attributes in models.items():
        for size, supported_roles in model_attributes.items():
            yaml_content = f"""---
name: {model_name.lower()} {size.lower()}
version: {version}
models:
- name: {model_name.lower()} {size.lower()}
  provider: ollama
  model: {model_name.lower()}:{size.lower()}
  roles:\n"""

            for role in supported_roles:
                yaml_content += f"    - {role.lower()}\n"

            file_path = os.path.join(base_path, f"{model_name}-{size}.yaml")
            try:
                with open(file_path, 'w') as file:
                    file.write(yaml_content)
                logging.info(f"Created YAML file for {model_name} {size}: {file_path}")
            except IOError as e:
                logging.error(f"Failed to write file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate YAML files for models.")
    parser.add_argument('--version', default=DEFAULT_VERSION, help='Version string for the YAML files')

    args = parser.parse_args()
    create_yaml_files(models, args.version)

if __name__ == "__main__":
    main()