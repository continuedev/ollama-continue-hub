#!/usr/bin/env python3

import os
import logging
import argparse

DEFAULT_VERSION = "1.0.6"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the models and their capabilities
models = {
    "gemma": {
        "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]}
    },
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
    "qwen3-coder": {
        "30b": {"roles": ["chat", "edit", "apply"], "capabilities": ["tool_use"]}
    },
    "gemma2": {
        "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "9B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "27B": {"roles": ["chat", "edit", "apply"]}
    },
    "gemma3": {
        "1B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "4B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "12B": {"roles": ["chat", "edit", "apply"]},
        "27B": {"roles": ["chat", "edit", "apply"]}
    },
    "codegemma": {
        "2B": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]}
    },
    "deepcode": {
        "1.5B": {"roles": ["chat", "edit", "apply"]},
        "14B": {"roles": ["chat", "edit", "apply"]}
    },
    "deepseek-r1": {
        "1.5b": {"roles": ["chat", "edit", "apply"]},
        "7b": {"roles": ["chat", "edit", "apply"]},
        "8b": {"roles": ["chat", "edit", "apply"]},
        "14b": {"roles": ["chat", "edit", "apply"]},
        "32b": {"roles": ["chat", "edit", "apply"]}
    },
    "granite-embedding": {
        "30m": {"roles": ["embed"]},
        "278m": {"roles": ["embed"]}
    },
    "nomic-embed-text": {
        "latest": {"roles": ["embed"]}
    },
    "llama3.1": {
        "8b": {"roles": ["chat", "edit", "apply"]},
        "70b": {"roles": ["chat", "edit", "apply"]}
    },
    "llama3.2": {
        "1b": {"roles": ["chat", "edit", "apply"]},
        "3b": {"roles": ["chat", "edit", "apply"]}
    },
    "mistral": {
        "7b": {"roles": ["chat", "edit", "apply"]},
    },
    "qwen2.5-coder": {
        "1.5b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "3b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "7b": {"roles": ["chat", "edit", "apply", "autocomplete"]},
        "14b": {"roles": ["chat", "edit", "apply"]},
        "32b": {"roles": ["chat", "edit", "apply"]}
    },
    "gpt-oss": {
        "20b": {"roles": ["chat", "edit", "apply"], "capabilities": ["tool_use"]},
        "120b": {"roles": ["chat", "edit", "apply"], "capabilities": ["tool_use"]}
    }
}

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
        for size, model_config in model_attributes.items():
            # Handle both old format (list) and new format (dict) for backward compatibility
            if isinstance(model_config, list):
                supported_roles = model_config
                capabilities = []
            else:
                supported_roles = model_config.get("roles", [])
                capabilities = model_config.get("capabilities", [])
            
            yaml_content = f"""---
name: {model_name.lower()} {size.lower()}
version: {version}
schema: v1
models:
- name: {model_name.lower()} {size.lower()}
  provider: ollama
  model: {model_name.lower()}:{size.lower()}
  roles:\n"""

            for role in supported_roles:
                yaml_content += f"    - {role.lower()}\n"
            
            # Add capabilities section if any capabilities are defined
            if capabilities:
                yaml_content += "  capabilities:\n"
                for capability in capabilities:
                    yaml_content += f"    - {capability.lower()}\n"

            file_path = os.path.join(base_path, f"{model_name.lower()}-{size.lower()}.yaml")
            try:
                with open(file_path, 'w') as file:
                    file.write(yaml_content)
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
