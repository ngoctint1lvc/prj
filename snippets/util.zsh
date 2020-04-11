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