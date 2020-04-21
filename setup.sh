#!/bin/bash

default_shell=$(grep $USER /etc/passwd | cut -f 7 -d ":")

echo "[+] Cloning repository";
if [ ! -e ~/.prj ]; then
    git clone https://github.com/ngoctint1lvc/prj.git ~/.prj
else
    (cd ~/.prj && git pull)
fi

echo "[+] Checking your python version and install required packages";
if [ -n "$(which python3)" ]; then
    (cd ~/.prj && python3 -m pip install -r requirement.txt)
elif [ -n "$(which python)" ] && [[ "$(python -V 2>/dev/null)" =~ "Python 3" ]]; then
    (cd ~/.prj && python -m pip install -r requirement.txt)
else
    echo "[+] Please install python3";
    exit -1;
fi

echo "[+] Detect default shell: $default_shell";

echo "[+] Auto load util script in your shell";
if [[ "$default_shell" =~ "zsh" ]]; then
    if [ -z "$(grep 'source ~/.prj/snippets/util.zsh' ~/.zshrc)" ]; then
        echo 'source ~/.prj/snippets/util.zsh' >> ~/.zshrc
    fi
elif [[ "$default_shell" =~ "fish" ]]; then
    if [ ! -d ~/.config/fish ]; then
        mkdir -p ~/.config/fish;
    fi

    if [ ! -f ~/.config/fish/config.fish ]; then
        touch ~/.config/fish/config.fish;
    fi
    
    if [ -z "$(grep 'source ~/.prj/snippets/util.fish' ~/.config/fish/config.fish)" ]; then
        echo 'source ~/.prj/snippets/util.fish' >> ~/.config/fish/config.fish
    fi
else
    if [ -z "$(grep 'source ~/.prj/snippets/util.sh' ~/.bashrc)" ]; then
        echo 'source ~/.prj/snippets/util.sh' >> ~/.bashrc
    fi
fi

if [ ! -f ~/.prj/config.json ]; then
    echo "[+] Config file not detected";
    echo "[+] Create your config file at ~/.prj/config.json";
    cat <<AAA > ~/.prj/config.json
[
    "$HOME",
    "$HOME/*",
    "$HOME/*/*",
    "$HOME/*/*/*"
]
AAA
    echo "[+] You can change this config at ~/.prj/config.json";
    cat ~/.prj/config.json;
else
    echo "[+] Config file detected at ~/.prj/config.json";
    echo "[+] Keeping your config file";
fi

echo "[+] Done! Try restarting your shell"