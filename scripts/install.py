import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).parent


def pyinstall():
    name = "prevedict"
    if (BASE_DIR / (f"{name}.spec")).exists():
        command = f"pyinstaller {name}.spec --noconfirm"
    else:
        command = (
            "pyinstaller prevedict/main.py"
            f" --name {name}"
            " --contents-directory data"
            " --add-data=prevedict/assets:assets"
            " --noconfirm"  # doesn't require override confirmation
        )

    process = subprocess.run(
        command,
        text=True,
        shell=True,
    )

    return process.returncode
