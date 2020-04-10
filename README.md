# Prj tool
Quickly navigate between your projects

## How to install

Clone this repo
```
git clone https://github.com/ngoctint1lvc/prj.git
```

Add directories where you put your projects into `config.json` file (absolute path)
```json
[
    "/path1",
    "/path1/*",
    "/path2/*"
]
```

Add this snippet into your `~/.zshrc` or `~/.bashrc`
```bash
prj () {
    cd $(python path_to_your_tool/project-finder.py $1 3>&1 1>$(tty) 2>/dev/null)
}
```

## Example usage
[![asciicast](https://asciinema.org/a/318215.svg)](https://asciinema.org/a/318215)