=======
 daily
=======
Hello and welcome to daily, a program for command-line journaling. Each
journal entry is stored in a file named after the date in YYYY-mm-dd format
in either MD or RST format.

Entries have a title named after the date, a desription, headings, and
metadata all built in to the text. Here is a simple example in markdown.

::

    # 2022-10-10, Mon
    I went to my daughter's play.

    ## Workout
    And did like a gazillion pushups.


    <!--- attributes --->
        ---
        id: some-internal-id
        tags: []

And an example in RST.

::

    =================
     2022-10-10, Mon
    =================
    This semester in college is really starting to grind.

    Todo
    ====
    - 8am Calculus class.
    - 9am Workout

    
    .. code-block:: yaml
    
        ---
        id: some-internal-id
        tags: []

Usage with Vimwiki 
===================
Modify daily.ini (installed in ``~/.config/daily`` after a first run) to change
the journal's directory to your vimwiki diary, and be sure the format is "md".

Also install the ``generate-vimwiki-diary-template`` file to your ~/.vim/bin
directory. This will make it so vim auto-generates daily's entry text for new
markdown files in the vimwiki diary directory. This must be done manually.

Usage
=====
Usage is detailed in the man pages under ``./doc/man``. Start with ``daily.1``,
but a general quick start cookbook...

::

    daily  # Perform first-time setup
    daily add  # Edit today's entry.
    daily show  # Show previous 2 weeks of entries
    daily add -d yesterday  # Add or edit an entry on a specific date.
    daily add --before today  # Batch edit any entries before today
    daily show workout todo  # Show only specific headings for entries
    daily add workout  # Edit specific headings for an entry.

    daily todo  # Print next 2 weeks of todos

Required packages for a developer
=================================
The machine used to develop this software was running Ubuntu 20.04. The
following packages are needed to build, develop, and package releases on
this operating system.

::

    python3-venv python3-pip dh-python docutils-common

Maintenance and versioning
==========================
Update the CHANGELOG when cutting a new release, then create and push a git tag
named after the new version. This project's packaging script and setup.py will
automatically determine the version based on git-describe.

Daily uses `semantic versioning <https://semver.org/>`_. Update the major
number if a breaking change is introduced with respect to the command-line
interface or expected entry format. Minor number for backwards-compatible
feature additions, and patch number for bugfixes or optimizations.

Building and installation
=========================
Clone this repo, checkout a release tag, and run these commands.

::

    ./package.bash python3
    pip3 install --user .
    ./package.bash clean

The ``package.bash`` script can also package the software as a python wheel or
a gz archive with the respective commands.

The man pages will be installed at ``$HOME/.local/usr/share/man``
and the bash completion script will be installed at
``$HOME/.local/etc/bash_completion.d/daily_completion.sh``. Update your bashrc.

Testing and developer usage
===========================
Run these commands to install daily to a virtual environment.

::

    python3 -m venv ./venv
    . ./venv/bin/activate
    python3 ./setup.py
    pip3 install -e .
    daily

Use the following command to run unit tests.

::

    python3 -m unittest

Known issues
------------
Daily generally works as expected. That said, there are a few bugs. These
shouldn't be a problem unless the user intentionally feeds bad input, but
nonetheless...

- General robustness with bad input and better error messages.
