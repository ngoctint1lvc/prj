# Prj tool
Quickly navigate between your projects

## How to install

Clone this repo
```
git clone https://github.com/ngoctint1lvc/prj.git
```

Add `config.json` file
```json
[
    "path1", // directories in where you put your projects
    "path2"
]
```

Add this snippet into your `~/.zshrc` or `~/.bashrc`
```bash
prj () {
    cd $(<path to your tool>/project-finder.py $1 3>&1 1>$(tty) 2>/dev/null)
}
```

## Example usage
[![asciicast](https://asciinema.org/a/318215.svg)](https://asciinema.org/a/318215)