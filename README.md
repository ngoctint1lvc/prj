# Prj tool
Quickly navigate between your projects

## How to install

Clone this repo and install missing packages
```
git clone https://github.com/ngoctint1lvc/prj.git
cd prj
pip3 install -r requirement.txt
```

Add directories where you put your projects into `config.json` file (absolute path or relative path)
```json
[
    "/path1",
    "/path1/*",
    "/path2/*",
    "./*"
]
```

Add this snippet into your `~/.zshrc` or `~/.bashrc` (modify your corrected path)
```bash
# nt tool
ntfind () {
    echo -n $(/usr/bin/python3 /your_path/prj/project-finder.py $@ 3>&1 1>$(tty) 2>/dev/null)
}

ntcode () {
    local dir=$(ntfind $@);
    [ -e "$dir" ] && code $dir
}

prj () {
    local dir=$(ntfind $@);
    [ -d "$dir" ] && cd $dir
}
```

If you are using fish shell, add this snippet to `~/.config/fish/config.fish` (create if file not exists)
```fish
# nt tool
function ntfind
    echo -n (/usr/bin/python3 /your_path/prj/project-finder.py $argv 3>&1 1>(tty) 2>/dev/null)
end

# only work if you installed vscode
function ntcode
    set -l dir (ntfind $argv);
    [ -e "$dir" ] && code $dir
end

function prj
    set -l dir (ntfind $argv);
    [ -d "$dir" ] && cd $dir
end
```

Add more useful functions for your need!

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