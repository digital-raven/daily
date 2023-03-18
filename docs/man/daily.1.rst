=======
 daily
=======

---------------------------
For command-line journaling
---------------------------

.. include:: _manual-section.rst

SYNOPSIS
========
**daily** [global-opts] *command* [options]

DESCRIPTION
===========
Daily is a program for command-line journaling. One can enter daily entries,
assign tags to entries, and go back to view entries within specified filtering
criterion.

Use the ``daily add`` command to add new entries or modify existing entries,
and the ``daily show`` command to go back to view those entries. Daily can also
be used to show upcoming events with the ``dailiy todo`` command. This
command will show entries in the near future if an entry has content added under
an "todo" heading. Each subcommand has its own manual page with more detail.

OPTIONS
=======
These global options must be specified before the subcommand.

**-h, --help**
        Show a help message and exit.

**--config** *CONFIG*
        Select custom configuration file. This configuration file is in ini
        format, and the default is at ~/.config/daily/daily.ini.

**-j, --journal** *JOURNAL*
        Specify the directory to store entries. The default journal is located
        in ~/.local/share/daily/

**-f, --entry-format** *FORMAT*
        What text format to use when displaying or editing entries. Choices are
         "md" or "rst".

**--version**
        Display the version of daily.

JOURNAL FORMAT
==============
Daily works by modifying and reading entries from a directory. The entries
may be in RST or markdown format. Each entry also has some metadata that may be
written at the bottom in yaml format. The following is an example in markdown.

::

    # 2021-07-06, Tues
    Notes appear just below the title.

    ## todo

    - [X] Get groceries


    <!--- attributes --->
        ---
        id: internal-id
        tags: [tags, go, here]

And the "add" subcommand allows users to modify entries by editing the
generated text.

FAQ
===

Manpages and auto-complete?
---------------------------
If daily was pip installed with the --user flag, then the man pages will be
installed at ``$HOME/.local/usr/share/man`` and the bash completion script
will be installed at ``$HOME/.local/etc/bash_completion.d/daily_completion.sh``.
Update your bashrc to source the completion script and update your ``MANPATH``
environment variable.

How do you say "hello" in Spanish?
----------------------------------
"Donde hello".

SEE ALSO
========
daily-add(1)
daily-show(1)
daily-todo(1)
