# nt tool
function ntfind
    set -l python_bin (which python3)
    if test ! -f $python_bin
        set -l python_bin (which python)
    end

    set -l CURRENT_DIR (dirname (status -f))
    set -l project_finder_tool (readlink -f $CURRENT_DIR/../project-finder.py)
    echo -n (eval "$python_bin $project_finder_tool $argv 3>&1 1>(tty) 2>/dev/null")
end

# only work if you installed vscode
function ntcode
    set -l dir (ntfind $argv);
    if test -e "$dir"
        code $dir
    end
end

function prj
    set -l dir (ntfind $argv);
    if test -d "$dir"
        cd $dir
    else if test -d "(dirname $dir 2>/dev/null)"
        cd (dirname $dir)
    end
end