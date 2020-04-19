local PRJ_DIR=$(readlink -f $(dirname $0)/..)

# nt tool
ntfind () {
    local python_bin="$(which python3)"
    local project_finder_tool="$(readlink -f $PRJ_DIR/project-finder.py)"
    echo -n $($python_bin $project_finder_tool $@ 3>&1 1>$(tty) 2>/dev/null)
}

ntcode () {
    local dir=$(ntfind $@);
    [ -e "$dir" ] && code $dir
}

prj () {
    local dir=$(ntfind $@);
    if [ -d "$dir" ]
    then
        cd $dir
    elif [ -d "$(dirname $dir 2>/dev/null)" ]
    then
        cd $(dirname $dir)
    fi
}