=======
 daily
=======
Hello and welcome to daily, a program for command-line journaling. Each
journal entry is stored in a file named after the date in YYYY-mm-dd format
in either MD or RST format.

Building and installation
=========================
Available via PyPi. ``pip3 install daily-cli --user``

Alternatively, clone this repo and run these commands.

::

    make
    pip3 install --user .

The man pages will be installed at ``$HOME/.local/usr/share/man``
and the bash completion script will be installed at
``$HOME/.local/etc/bash_completion.d/daily_completion.sh``. Update your bashrc.

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
-------------------
Modify daily.ini (installed in ``~/.config/daily`` after a first run) to change
the journal's directory to your vimwiki diary, and be sure the format is "md".

Also install the ``generate-vimwiki-diary-template`` file to your ~/.vim/bin
directory. This will make it so vim auto-generates daily's entry text for new
markdown files in the vimwiki diary directory. This must be done manually.

Maintenance and versioning
==========================
Update the CHANGELOG when cutting a new release, then update the version
in setup.py. Then commit and tag it named after the release. Then...

- Run ``make`` to build the package.
- ``make release`` to upload to PyPi.
