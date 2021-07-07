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
The "add" subcommand is used to add a new entry to a journal or edit an
existing one.

This command will search for the entry specified by the **--date** flag (or
"today", if **--date** was not provided) and open the text editor in the
**EDITOR** or **VISUAL** environment variables to modify the entry. The entry
will be displayed in RST format for editing. Then the user makes her edits and
the resulting RST will be re-entered into the journal upon saving and exiting
the text editor.

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

**-h**, **--help**
        Display a help message and exit.

**-d, --date** *DATE*
        Select the entry for a specific date. The default is "today". Dates may
        be entered in plain english, so entries like "tomorrow", or "2 weeks ago",
        or "2 weeks from now" are acceptable.

EXAMPLES
========
Each entry has a title, headings, and tags. Any headings will automatically
become tags upon entry. Tags may be manually specified on the last line of
the entry after the "tags:" keyboard. Don't forget the colon.

To add a new entry for "today", simply run ``daily add``, and some text like
the following will be displayed in a text editor in RST format.

::

    2021-07-04, Sun
    ===============

    tags:

Any text added immediately follwing the title will be stored under the "notes"
heading. To add text under different headings, specify the heading as a
level-2 RST heading as follows.

::

    2021-07-04, Sun
    ===============
    My family and I enjoyed the fireworks.

    Workout
    -------
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.

    tags:

The above example will store the text under the "workout" heading within the
journal file. If we go back to edit that entry (or see it via the "show"
command"), it would look like this.

::

    2021-07-04, Sun
    ===============
    My family and I enjoyed the fireworks.

    Workout
    -------
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.

    tags: workout

Notice that "workout" was automatically added to the entry's tags. Daily will
automatically add tags for each heading in an entry. The tags are generated
by downcasing the headings and replacing the spaces with dashes ("-").

If we wanted to just modify the "Workout" heading, we would use the command
``daily add -d "July 4th 2021" workout``, and then only the workout heading
would appear in the user's text editor. Headings are not case-sensitive.

::

    2021-07-04, Sun
    ===============
    Workout
    -------
    - 100 push ups, 100 sit-ups, 100 squats, and a 10Km run.

    tags: workout

Though it is possible to add other headings manually. Just follow the expected
RST format. Non-existent headings may also be provided to the command, and they
will be created.

SEE ALSO
========
daily(1)
