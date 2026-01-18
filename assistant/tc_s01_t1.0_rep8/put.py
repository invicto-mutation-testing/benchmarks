from pathlib import Path
import yaml
from colorama import Fore

"""
Use Case S-01)
Entwicklung von einem Hilfs-Modul mit statischen Funktionen zum Beispiel eine utils.py Datei mit Verwendung von 3rd party libraries.
Eingabe einer statischen Funktion
autogpts utils.py
"""


def validate_yaml_file(file: str | Path):
    try:
        with open(file, encoding="utf-8") as fp:
            yaml.load(fp.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        return (False, f"The file {Fore.CYAN}`{file}`{Fore.RESET} wasn't found")
    except yaml.YAMLError as e:
        return (
            False,
            f"There was an issue while trying to read with your AI Settings file: {e}",
        )

    return (True, f"Successfully validated {Fore.CYAN}`{file}`{Fore.RESET}!")

