import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "rtcomm"

list_of_files = [
    f"notebooks/experiments.ipynb",
    f"logs/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/core/__init__.py",
    f"src/{project_name}/core/config.yaml",
    f"src/{project_name}/core/config.py",
    f"src/{project_name}/core/constants.py",
    f"src/{project_name}/core/params.yaml",
    f"src/{project_name}/core/prompts.py",
    f"src/{project_name}/data/__init__.py",
    f"src/{project_name}/data/raw/__init__.py",
    f"src/{project_name}/data/processed/__init__.py",
    f"src/{project_name}/data/interim/__init__.py",
    f"src/{project_name}/handlers/__init__.py",
    f"src/{project_name}/handlers/output_generator.py",
    f"src/{project_name}/handlers/custom_exceptions.py",
    f"src/{project_name}/models/__init__.py",
    f"src/{project_name}/services/__init__.py",
    f"src/{project_name}/services/langchain_framework.py",
    f"src/{project_name}/schemas/__init__.py",
    f"src/{project_name}/schemas/config_schema.py",
    f"src/{project_name}/schemas/schema.yaml",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/helper_functions.py",
    f"src/{project_name}/utils/custom_logging.py",
    f"src/main.py",
    "Dockerfile",
    "requirements.txt",
    "pyproject.toml"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")