#!/bin/bash

thisdir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)


bindir='D:\bin'
envname='env'

_install()(
    cd "$thisdir" \
        && virtualenv "$envname" \
        && pip install -r 'requirements.txt'
)

runname='githubapi'
python=$thisdir/$envname/Scripts/python
scriptw=$(cygpath -w "$thisdir/client.py")
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
        && ln -sf "$thisdir/$runname" "$bindir"
)

_deploy




