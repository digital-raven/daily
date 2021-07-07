============
 daily-show
============

--------------------------------
Display entries from the journal
--------------------------------

.. include:: _manual-section.rst

SYNOPSIS
========

**daily** [global-opts] **show** [options] [*HEADING* ...]

DESCRIPTION
===========
Use this command to display entries from the Journal. Entries may be selected
based on specific filters, but by default the entries from "today" and the
previous 2 weeks will be shown.

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

.. include:: _daily-filter-opts.rst

SEE ALSO
========
daily(1)
