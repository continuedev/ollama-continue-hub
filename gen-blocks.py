#!/usr/bin/env python3

import os
import logging
import argparse
import yaml

DEFAULT_VERSION = "1.0.6"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the models and their capabilities
models = {
    # "gemma": {
    #     "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]}
    # },
    "qwen3": {
        "0.6B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "1.7B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "4B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "8B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "14B": {"roles": ["chat", "edit", "apply"]},
        "30B": {"roles": ["chat", "edit", "apply"]},
        "32B": {"roles": ["chat", "edit", "apply"]},
        "235B": {"roles": ["chat", "edit", "apply"]},
    },
    "granite4": {
        "micro": {"roles": ["chat", "edit", "apply"]},
        "micro-h": {"roles": ["chat", "edit", "apply"]},
        "tiny-h": {"roles": ["chat", "edit", "apply"]},
        "small-h": {"roles": ["chat", "edit", "apply"]},
    },
    # "gemma2": {
    #     "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "9B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "27B": {"roles": ["chat", "edit", "apply"]}
    # },
    # "gemma3": {
    #     "1B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "4B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "12B": {"roles": ["chat", "edit", "apply"]},
    #     "27B": {"roles": ["chat", "edit", "apply"]}
    # },
    # "codegemma": {
    #     "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]}
    # },
    # "deepcode": {
    #     "1.5B": {"roles": ["chat", "edit", "apply"]},
    #     "14B": {"roles": ["chat", "edit", "apply"]}
    # },
    # "deepseek-r1": {
    #     "1.5b": {"roles": ["chat", "edit", "apply"]},
    #     "7b": {"roles": ["chat", "edit", "apply"]},
    #     "8b": {"roles": ["chat", "edit", "apply"]},
    #     "14b": {"roles": ["chat", "edit", "apply"]},
    #     "32b": {"roles": ["chat", "edit", "apply"]}
    # },
    # "granite-embedding": {
    #     "30m": {"roles": ["embed"]},
    #     "278m": {"roles": ["embed"]}
    # },
    # "nomic-embed-text": {
    #     "latest": {"roles": ["embed"]}
    # },
    # "llama3.1": {
    #     "8b": {"roles": ["chat", "edit", "apply"]},
    #     "70b": {"roles": ["chat", "edit", "apply"]}
    # },
    # "llama3.2": {
    #     "1b": {"roles": ["chat", "edit", "apply"]},
    #     "3b": {"roles": ["chat", "edit", "apply"]}
    # },
    # "mistral": {
    #     "7b": {"roles": ["chat", "edit", "apply"]}
    # },
    # "qwen2.5-coder": {
    #     "1.5b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "3b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
    #     "14b": {"roles": ["chat", "edit", "apply"]},
    #     "32b": {"roles": ["chat", "edit", "apply"]}
    # },
}

class IndentArrayDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentArrayDumper, self).increase_indent(flow, False)

def create_yaml_files(models, version, family=None):
    base_path = './blocks/public'

    # Create the directory if it doesn't exist
    try:
        os.makedirs(base_path)
    except FileExistsError:
        pass

    # Filter models by family if specified
    if family:
        if family not in models:
            logging.error(f"Family '{family}' not found in models dictionary.")
            return
        models_to_process = {family: models[family]}
    else:
        models_to_process = models

    for model_name, model_attributes in models_to_process.items():
        for size, properties in model_attributes.items():
            # Create YAML document structure
            yaml_data = {
                "name": f"{model_name.lower()} {size}",
                "version": version,
                "schema": "v1",
                "models": [
                    {
                        "name": f"{model_name.lower()} {size}",
                        "provider": "ollama",
                        "model": f"{model_name.lower()}:{size}"
                    }
                ]
            }

            # Add properties to the model
            model_config = yaml_data["models"][0]
            for prop_name, prop_value in properties.items():
                model_config[prop_name] = prop_value

            # Convert roles to lowercase if present
            if "roles" in model_config:
                model_config["roles"] = [role.lower() for role in model_config["roles"]]
            file_path = os.path.join(base_path, f"{model_name.lower()}-{size.lower()}.yaml")
            try:
                with open(file_path, 'w') as file:
                    # Use PyYAML to dump the data
                    yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False, indent=2, Dumper=IndentArrayDumper)
                logging.info(f"Created YAML file for {model_name} {size}: {file_path}")
            except IOError as e:
                logging.error(f"Failed to write file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate YAML files for models.")
    parser.add_argument('--version', default=DEFAULT_VERSION, help='Version string for the YAML files')
    parser.add_argument('--family', help='Only generate YAML files for a specific model family')

    args = parser.parse_args()
    create_yaml_files(models, args.version, args.family)

if __name__ == "__main__":
    main()
