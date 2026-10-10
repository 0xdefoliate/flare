# flare
Read Flarum discussions in your Terminal.

**NOTE:** This project is *not* stable by any means, and is in active development.  
Thus, do not expect a bug-free polished product.

## Usage

```bash
# change the second argument to another origin if you want to read a different Flarum server.
$ flare discuss.grapheneos.org
```

## Installation

No bundled versions for swift distribution currently exists, and you have to manually clone it yourself.

Follow these instructions:
1. Clone this repo with `git` and `cd` into it.
2. Create a `.venv` via `$ python -m venv .venv`.
3. `$ . .venv/bin/activate`
4. `$ pip install -r requirements.txt`
5. `$ pip install .`
6. Done.

The executable script will get removed from the virtual environment when you quit it.  
A more sophisticated installation procedure for more convenient use is planned soon.

## Security

### Sandboxing

To improve the runtime security of this application, the application intends to be run sandboxed.
However, as of the time of writing, only sandboxing on macOS is supported.

You can see what gets enforced in `src/flare/sandbox_policy/macos`.

Sandboxing for other operating systems is planned.

## Rationale

This project was inspired by [this project](https://github.com/JohnnyLoansEsquire/Flarum_Discussion_Downloader)'s concept.  
However, that project has multiple issues (as of the time of writing):
1. It's "vibecoded", which is problematic due to:
   * Copyright: there is no guarantee the LLM hasn't outputted GPL'd or proprietary code, or similar.
   * Ethics: do your homework, I am not gonna write a thesis here.
2. It's shell-script. This may not be much of an issue *now*, but it is just a question of time until it becomes a big-ball-of-mud due to it not being a proper programming language.
3. It utilises bad coding practices like shell variables in `SCREAMING_SNAKE_CASE`, no functions at all, no checks of commands being installed, etc.

Hence, I decided to make this project, which is written in Python instead.
