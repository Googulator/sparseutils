sparseutils
-----------

A collection of utilities for interacting with sparse files.

Installation
------------

You can install sparseutils with pip,

    % sudo pip3 install sparseutils

alternatively you can clone the [source]
and then run pip from within the git repo:

    % sudo pip3 install .

you can also run the tests from within the git repo using tox:

    % tox

Contributing
------------

To report an issue you can email me, please see the git log for the address.

Patches welcome! To prepare a patch series:

    % git format-patch --cover-letter -o patch -M origin/master
    % $EDITOR patch/0000-cover-letter.patch
    % git send-email patch

[source]: http://git.gitano.org.uk/personal/richardipsum/sparseutils.git
