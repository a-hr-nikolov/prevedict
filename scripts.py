import pathlib
import re
import subprocess


def benchmark():
    runs = 15
    total = 0
    print("----------------------")
    print("Launch time averages:")
    print("----------------------")
    for i in range(runs):
        result = subprocess.run(
            ["python", "tests/benchmark.py"], capture_output=True, text=True
        )
        str_num = re.search(r"\d\.\d{,3}", result.stdout)
        current = float(str_num.group(0))
        total += current
        print(f"Run {i+1}/{runs}: {current:0.3f} seconds", flush=True)

    print("----------------------")
    print(f"Average: {total / runs:0.3f} seconds")


def pyinstall():
    name = "prevedict"
    if pathlib.Path(f"{name}.spec").exists():
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
