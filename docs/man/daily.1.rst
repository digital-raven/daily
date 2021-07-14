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
be used to show upcoming events with the ``dailiy upcoming`` command. This
command will show entries in the near future if an entry has content added under
an "events" heading. Each subcommand has its own manual page with more detail.

OPTIONS
=======
These global options must be specified before the subcommand.

**-h, --help**
        Show a help message and exit.

**--config** *CONFIG*
        Select custom configuration file. This configuration file is in ini
        format, and the default is at ~/.config/daily/daily.ini.

**-j, --journal** *JOURNAL*
        Specify the journal to operate on. The default journal file is located
        in ~/.local/share/daily/journal.json.

JOURNAL FORMAT
==============
Daily works by modifying and reading a journal file. It is not expected for a
user to modify the journal file themselves; leave it to the "add" command.
The journal file is in json format, and follows the structure below.

::

    [
        {
            "title": "2021-07-06, Tues",
            "headings": {
                "notes": "Notes appear just below the title.",
                "work": "And some stuff happened at work."
            },
            "tags": [
                "work"
            ]
            "id": "f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-06_13-44-39-905973"
        },
        ...
    ]

When displayed back, daily will format these entries into RST text. The above
entry would appear as follows:

::

    2021-07-06, Tues
    ================
    Notes appear just below the title.

    Work
    ----
    And some stuff happened at work.

    id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-19_13-44-39-905973
    tags: work

And the "add" subcommand allows users to modify entries by editing the
generated RST.

FAQ
===
Why RST?
~~~~~~~~
It's my favorite text format and pairs excellently with vim.

Why JSON instead of storing entries in plain RST?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSON allows separating out tags and entries, and easier loading into
memory for searching and sorting. The features of "daily" would not
be possible if the data were not easy to read from the journal.

Future development?
~~~~~~~~~~~~~~~~~~~
If there's interest. I was going to add more features, but I wanted this to
be a quick project, and it's currently usable for its basic purpose. If someone
sees promise in this and wants to contribute or make a feature suggestion, feel
free to open a PR or email me.

How do you say "hello" in Spanish?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"Donde hello".

SEE ALSO
========
daily-add(1)
daily-refresh(1)
daily-show(1)
daily-upcoming(1)
