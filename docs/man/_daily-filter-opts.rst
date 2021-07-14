FILTER OPTIONS
--------------
Options for filtering entries. Dates may be entered in plain english, so
phrases like "today", or "2 weeks from now", or "5 months ago" are acceptable.

The underlying JSON file that contains a journal also associates each with
an ID. Do not use this ID for any operations. These IDs are subject to
change depending on how the underlying entries were modified. Only use the
title of an entry, which is the same as its date. This is guaranteed to be
unique.

**--after** *DATE*
        Filter for entries after a date.

**--before** *DATE*
        Filter for entries before a date.

**-d, --date** *DATE*
        Filter for entries on a specific date.

**--tags** *TAGS*
        Filter for entries that involve the specified tags.
