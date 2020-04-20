# Prj tool
Quickly navigate between your projects

## How to install

Run this command for auto setup
```bash
curl https://raw.githubusercontent.com/ngoctint1lvc/prj/master/setup.sh | bash -
```

For Mac user, readlink is incompatible with gnu readlink, simply install coreutils to fix this problem
```bash
brew install coreutils
echo 'export PATH=/usr/local/opt/coreutils/libexec/gnubin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Add directories where you put your projects into `~/.prj/config.json` file (absolute path or relative path)
```json
[
    "/home/",
    "/home/*",
    "/home/*/*",
    "/home/*/*/*"
]
```

## Example usage
[![asciicast](https://asciinema.org/a/318215.svg)](https://asciinema.org/a/318215)

### Example 1: To list all available options, run this command
```bash
> prj --help
usage: project-finder.py [-h] [-c CONFIG] [-d MAXDEPTH] [-l LIMIT] [-v]
                         [searchDir [searchDir ...]]

Project finder utility for cli user

positional arguments:
  searchDir             custom search directories

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        custom config file
  -d MAXDEPTH, --max-depth MAXDEPTH
                        maximum depth to search (only affected when providing
                        searchDir arguments)
  -l LIMIT, --limit LIMIT
                        limit number of results
  -v, --verbose         verbosity (for debugging purpose)
```

### Example 2: search in specific directories with custom depth level
```bash
> prj . /tmp/ -d 3
```

### Example 3: run command after search
```bash
> ls -l $(ntfind)
```