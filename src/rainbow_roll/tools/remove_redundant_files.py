from gapi import remove_redundant_files

from rainbow_roll.constants import FILES_PATH

if __name__ == "__main__":
    for model in FILES_PATH.iterdir():
        if model.name == ".git":
            continue

        json_files = list(model.glob("*.json"))
        remove_redundant_files(json_files)
