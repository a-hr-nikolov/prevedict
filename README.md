# Prevedict - An EN-BG Dictionary

Prevedict is a quick word-based EN-BG (bi-directional) dictionary. It automatically displays the closest word (in alphabetical order) that starts with the input query, and the result gets updated on each keystroke.

Prevedict is intended as a modern and lightweight alternative to SA Dictionary. I've developed it primarily for Linux, but it can be used on Windows as well. It works as a snappy pop-up app that can be mapped to a key shortcut (e.g. Ctrl+Win+Alt+D), opened immediately, run for a second, and then closed with another shortcut (e.g. Alt+F4, or Ctrl+Q).

## Why not Google Translate?

Simply put, Prevedict has a different goal. While GT works, it fails in one major way - speed. In fact, I tried turning Google Translate into a Progressive Web App, but it was slow to open and operate, often requiring manual configuration (e.g. picking languages). Of course, that is because it has to be flexible with languages, text, etc. Which would be great, if that's what I need, but 99% of the time it isn't. I want to check a specific word, perhaps some use cases, maybe the transcription, or maybe just the correct spelling. So I don't require fancy sentence translation, or text-to-speech or whatever. I need something fairly simple (and quick), hence Prevedict.

## Installation Guide

There currently isn't a one-click installation. The plan is to provide install files for different platforms, but I currently don't have the time to package and test all of those, not to mention maintaining them if need be. So here is a fairly simple way to install the dictionary. Figuring out icons is shortcuts is up to you though.

### Pre-conditions: Poetry

Poetry is a virtual environment, dependency and package management tool for Python. Install it on your system. On Windows that would generally require having `pip` already installed, which comes bundled with any Python installation. So the command is as simple as `pip install poetry`. On Linux distros Poetry is usually its own package (e.g. for OpenSUSE that would be `pythonXX-poetry` where `XX` is the latest stable version).

Once Poetry is installed, make sure you set it up to create virtual environments at the project's root with `poetry config virtualenvs.in-project true`. With that set up, you can continue freely.

### Steps

Run the following commands from the **project root**:

1. `poetry install`
2. `poetry run pyinstall`

If this doesn't work for some reason, you can do `poetry shell` and run `pyinstaller prevedict.spec` manually.

The `dist/prevedict` directory should now exist. Within it you will see a `prevedict` executable. Use it to run the app. You can create a desktop file for it, or simply a shortcut, but since that is platform-specific, you'd have to figure that out for yourself.

## Developer Notes

### Why Python?

Python has a robust GUI development ecosystem, especially with its Qt bindings (PySide6 in my case). The app is also I/O-bound, meaning the language used wouldn't be as important for performance. Sure, Python could be a bit bloated, but it works, and is great for simple project such as this one. Python also has the advantage of having a great interface for data manipulation, making it useful for one-shot tasks (e.g. all the modules in the `processors` directory).

### Data Source

As an initial source for this dictionary I have used the data of [BG Office](https://bgoffice.sourceforge.net/), which can be accessed at the [Bulgarian Language Support SourceForge Repository](https://sourceforge.net/projects/bgoffice/).

The thesaurus functionality comes from [Dictionary API](https://dictionaryapi.dev/), paired with [Datamuse](https://datamuse.com/) for word completion.

#### A note about the raw data

I've transcoded the raw data to UTF-8, making it easier to read with standard text editors. I've replaced the null characters with `###\n`.

I've also loaded the data as Python objects, then pickled those to save on some processing time during startup. However, it is a good security practice to only unpickle things you trust. So, if you prefer, you can use the pickling script in the `processors` directory to pickle the raw data yourself.

### Challenges along the way

#### Weird data

While the data consists mostly of single-word entries, it also has quite a few exceptions and edge cases. Not accounting for those in the beginning resulted in some weird behavior.

It all started with two-word entries (e.g. `WORKING CLASS`). I had to not allow spaces as valid characters. Then I found some dashed words (e.g. `WORK-OUT`), so I had to make dashes valid, too. Though I'd argue a lot of those dashed words are outdated (e.g. `WORK-BOX`, `WAIST-BAND`, `BABY-SITTER` can all be single words).

Lastly, some words use apostrophes (e.g. `NE'ER`)... Who would have thought! This was the hardest to catch, as there are only a few of those words in the dataset, and I didn't even suspect it. I would occasionally get errors in the terminal, but the app didn't break. It only listed wrong suggestions, but that couldn't be caught when writing quickly, since they updated correctly on a valid word. However, it did bug me, so after paying more attention, I finally managed to reproduce the issue by writing `NE`, and not having `NE...` suggestions displayed.

Note: There are (admittedly very few) typos in the word entries. So far I haven't found a way to programmatically fix them. I tried running them through a thesaurus, but it flagged too many words as incorrect. For now, I'm manually fixing typos when I encounter them.

#### Functionality and package bloat

Currently, the app is quite snappy and responsive, but it still opens up more slowly than I'd like, and it's footprint is a bit too big.

## Possible future steps

- [ ] Implement the dictionary as a CLI/dmenu/rofi tool
- [ ] Figure out a better installation procedure
- [ ] Find a way to de-bloat the app (maybe through tree shaking, or something like that)

## LICENSE

GPL v3
