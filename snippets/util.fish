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