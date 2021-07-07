===============
 daily-refresh
===============

---------------------------------
Fix minor internal journal errors
---------------------------------

.. include:: _manual-section.rst

SYNOPSIS
========

**daily** [global-opts] **refresh**

DESCRIPTION
===========
This command can correct minor errors within a journal. These would be things
like a title not matching the proper date format, but was still a parsable
date, or perhaps a heading was internally up-cased. The journal will be read
into memory and then written back to disk, which should fix minor errors.

Only minor errors can be corrected in this fashion. Json syntax errors are not
correctable, for example.

CORRECTABLE ERRORS
------------------
This should not be considered a complete enumeration.

- Headings with caps.
- Tags that don't contain all headings.
- Titles in a non-standard format, but are still parsable dates.
- Unsorted entries.

OPTIONS
=======
These options must be specified after the subcommand.

**-h**, **--help**
        Display a help message and exit.

SEE ALSO
========
daily(1)
