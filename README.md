# Prj tool
Quickly navigate between your projects

## How to install

Clone this repo
```
git clone https://github.com/ngoctint1lvc/prj.git
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

Add this snippet into your `~/.zshrc` or `~/.bashrc`
```bash
prj () {
    cd $(python3 path_to_your_tool/project-finder.py $1 3>&1 1>$(tty) 2>/dev/null)
}
```

If you are using fish shell, add this snippet to `~/.config/fish/config.fish` (create if file not exists)
```fish
function prj
    cd (python3 path_to_your_tool/project-finder.py $1 3>&1 1>(tty) 2>/dev/null)
end
```

## Example usage
[![asciicast](https://asciinema.org/a/318215.svg)](https://asciinema.org/a/318215)