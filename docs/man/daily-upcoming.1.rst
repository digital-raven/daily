================
 daily-upcoming
================

----------------------
Display upcoming todos
----------------------

.. include:: _manual-section.rst

SYNOPSIS
========

**daily** [global-opts] **upcoming** [options]

DESCRIPTION
===========
This command shows upcoming todos. Any entries in the future which contain
content under a heading titled "todo" will be shown, and only the events
will be shown. By default, only entries on or after "today" within the next
2 weeks will be shown, but entries can be filtered differently.

OPTIONS
=======
These options must be specified after the subcommand.

**-h**, **--help**
        Display a help message and exit.

.. include:: _daily-filter-opts.rst

SEE ALSO
========
daily(1)
