===========
 daily-add
===========

-------------------------
Add or edit a daily entry
-------------------------

.. include:: _manual-section.rst

SYNOPSIS
========
**daily** [global-opts] **add** [options] [HEADING ...]

DESCRIPTION
===========
The "add" subcommand is used to add new entries to a journal or edit existing
ones.

This command will search for entries which match the filter arguments and open
the text editor in the **EDITOR** or **VISUAL** environment variables to modify
the entries. The entries will be displayed in RST or MD format for editing.
Then the user makes her edits and the resulting text will be re-entered into
the journal upon saving and exiting the text editor. If no filters were
provided then it will be assumed the user wishes to create a new entry for the
value of **-d, --date**, which defaults to "today". If filters were provided,
but no entries were found, then a message will be printed informing the user
that no matching entries were found.

The entries are expected in a certain format, but this command contains great
conveniences to make adding entries easy. These are detailed further in the
**EXAMPLES** section. If an entry did not match the expected format, then
the journal will not be modified and a helpful error message will be printed.

POSITIONAL ARGUMENTS
====================

*HEADING ...*
        Add (or modify) specific headings for an entry. Only the listed
        headings will be displayed. Headings are not case-sensitive.

OPTIONS
=======
These options must be specified after the subcommand.

**--copy-previous** [*date*]
        Create a new entry by copying from a previous entry, making it easier
        to keep up with goals and remember what **you said you would do**.

        *date* may be a date in some formal format or a plain english phrase
        like "yesterday" or "last week".  If an entry on this date is not
        found, then daily will walk up to a year back from *date* and pick the
        first entry it finds.

        If *date* isn't provided then the value defaults to "yesterday".

**-h**, **--help**
        Display a help message and exit.

.. include:: _daily-filter-opts.rst

EXAMPLES
========
Each entry has a title, headings, and metadata. The metadata is at the end of
an entry in yaml format.

To add a new entry for "today", simply run ``daily add``, and some text like
the following will be displayed in a text editor in RST or MD format.

Please note the auto-generated ID for the entry. Each entry will have one. **Do
not modify this ID**.

::

    =================
     2021-07-04, Sun
    =================


    .. code-block:: yaml

        ---
        id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-04_13-44-39-905973
        tags:

Any text added immediately follwing the title will be stored under the "notes"
heading. To add text under different headings, specify the heading as a
level-2 RST or Markdown heading as follows.

::

    =================
     2021-07-04, Sun
    =================
    My family and I enjoyed the fireworks.

    Workout
    =======
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.


    .. code-block:: yaml

        ---
        id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-04_13-44-39-905973
        tags:

The above example will store the text under the "workout" heading within the
journal file. If we go back to edit that entry (or see it via the "show"
command"), it would look like this.

::

    =================
     2021-07-04, Sun
    =================
    My family and I enjoyed the fireworks.

    Workout
    =======
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.


    .. code-block:: yaml

        ---
        id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-04_13-44-39-905973
        tags:

If we wanted to just modify the "Workout" heading, we would use the command
``daily add -d "July 4th 2021" workout``, and then only the workout heading
would appear in the user's text editor. Headings are not case-sensitive.

::

    =================
     2021-07-04, Sun
    =================

    Workout
    =======
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.


    .. code-block:: yaml

        ---
        id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-04_13-44-39-905973
        tags:

It is possible to add other headings manually; simply follow the expected
formats. Non-existent headings may also be provided to the command, and they
will be created.

To modify multiple entries, specify the filtering criterion. Let's filter for
all entries that contain the "workout" or "diet" tags.

::

    $ daily add --tags workout,diet

    =================
     2021-07-03, Sat
    =================

    Diet
    ====
    Ate BORGER. Big fat, much yum.


    .. code-block:: yaml

        ---
        id: b2c6da6f448c6362757e11194e3e78477d42afb6-2021-7-03_4-9-49-152227
        tags: diet

    .. end-entry

    =================
     2021-07-04, Sun
    =================
    My family and I enjoyed the fireworks.

    Workout
    =======
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.


    .. code-block:: yaml

        ---
        id: f559323bea5b7acf9f2e9e7ffd4871ff915e0956-2021-7-04_13-44-39-905973
        tags: workout


SEE ALSO
========
daily(1)
