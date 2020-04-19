# Prj tool
Quickly navigate between your projects

## How to install

Clone this repo and install missing packages
```
git clone https://github.com/ngoctint1lvc/prj.git ~/.prj
cd ~/.prj
pip3 install -r requirement.txt
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

Run this command if you are using bash shell
```bash
echo 'source ~/.prj/snippets/util.sh' >> ~/.bashrc
source ~/.bashrc
```

Similarly with zsh shell
```zsh
echo 'source ~/.prj/snippets/util.zsh' >> ~/.zshrc
source ~/.zshrc
```

If you are using fish shell
```fish
echo 'source ~/.prj/snippets/util.fish' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
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