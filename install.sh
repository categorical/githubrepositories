#!/bin/bash

thisdir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)


bindir='d:\bin'
envname='env'

runname='gitapi'
script=$thisdir/githubrepositories
python=$thisdir/$envname/Scripts/python
pip=$thisdir/$envname/Scripts/pip
scriptw=$(cygpath -w "$script")


_install()(
    cd "$thisdir" \
        && virtualenv "$envname" \
        && "$pip" install -r 'requirements.txt'
)



_deploy()(
    cd "$thisdir" \
        && { cat<<-EOF>"$runname"
		#!/bin/bash
		exec '$python' '$scriptw' \\
		EOF
        } \
        && { cat<<-EO'F'>>"$runname"
		"$@"
		EOF
        } \
        && chmod u+x "$runname" \
        && { [ ! -d "$bindir" ] \
            ||ln -sf "$thisdir/$runname" "$bindir";}

)


_usage(){
    local -r c1="$(printf '%b' '\033[1m')"
    local -r c0="$(printf '%b' '\033[0m')"
    cat <<-EOF
	${c1}SYNOPSIS${c0}
	    $0 ${c1}--install${c0}
	    $0 ${c1}--deploy${c0}
	EOF
}

case $1 in
    --install)_install;;
    --deploy)_deploy;;
    *)_usage;;
esac


