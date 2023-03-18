===========
 Changelog
===========
All notable changes to daily will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[2.0.2] - 2023-01-19
====================
Correct README installation instructions. Dang name conflict on PyPi.

[2.0.1] - 2023-01-19
====================
Fix to README format in setup.py

[2.0.0] - 2023-01-19
====================
Technically a breaking change with renaming the ``upcoming`` subcommand
to ``todo`` but I'll give it a scream test. Whose gonna scream?

Also now installed as ``daily-cli`` because ``daily`` was taken on PyPi.

Changed
-------
- Entries will be deleted if their whole text is removed during editing.
- ``upcoming`` is now ``todo``.
- Build procedure is different now.

Removed
-------
- ``refresh`` subcommand is now removed.

Refactor
--------
- Underlying entries now stored using libzet zettels.

[1.0.1] - 2023-01-19
====================
Some minor bugfixes and removal of debian packaging support. Pip should
be fine now.

Fixed
-----
- pip installation with --user . Users will have to update their MANPATH
  and possibly an edit to their bashrc to sort the completion correctly.

Removed
-------
- Packaging support for deb. Much too complicated.

[1.0.0] - 2022-12-05
====================
There are many changes to entry format from 0.4.0 to 1.0.0 . Porting entries
from previous versions of daily to 1.0.0 will require some work on part of
the user.

The main reason for this is compatibility with vimwiki, which has its own
complement of daily entry tools that store the entries in individual files, and
daily should not exclude the user from using these tools with their own entries.

The following are the general list of changes to individual entry format.

- No special separation strings are needed at the end of entry files. These will
  be generated automatically when displaying or editing multiple entries.
- RST titles are now level 1, proper titles with ``===`` borders on both above
  and below lines.
- The data at the bottom of an entry may now be arbitrarily stored in yaml
  format. daily has no tools to query based on these arbitrary information, but
  they will become available in a backwards compatible way.
- This data will now be properly displayed as a code-block when rendering.

The other features are preserved; per-heading display / editing, batch
editing of entries, etc...

To port your entries from an older version, run ``daily add`` with 1.0.0 to see
the new format, export your previous entries to plain text using ``daily show``
with the older version of daily, and massage the text however you need before
importing it with ``daily add`` aagin from version 1.0.0. Be sure to maintain
backups throughout this process. These are plaintext files; not reason not to
version with git.

Added
-----
- Command-line option to set entry format.
- Adding vim template generator and instructions.
- no_edit function. This can be used to generate a blank entry to stdout.
  Useful when combined with aforementioned vim template.
- General unit tests.
- Entries may now have arbitrary data stored at the end in yaml format.

Changed
-------
- BIG ONE: Individual files for entries.
- Totally changed expected entry format.
- Up-level RST headings.RST entries now use RST title blocks for the title
  rather than the `===` underline. Headings now use the `===` instead of `---`.
- Documentation updates.
- The temp file used by the editor is now created in the journal dir instead
  of /tmp. This ensures outbound file links will remain valid when the entry
  is complete.
- The "upcoming" command now looks for the "todo" heading instead of "events".
- Attributes are now displayed in a code block when the text is rendered.
- RST entries are now separated by break comments like md, and the MD entry
  separator is now ``<!--- end-entry --->``

Removed
-------
- Daily will no longer delete entries when those entries are removed during
  batch editing. This was necessary to conveniently remove entries when they
  were stored in a single json, but now users can use their own filesystem
  tools to remove entries.

[0.4.0] - 2022-09-28
====================
Added support for markdown. Markdown can be used by setting a line in daily's
ini file.

Funny enough the journal can switch between markdown and rst if one only uses
the 2 top-level headings expected for each format in daily. (=== and --- for
rst, # and ## for markdown). This interchange will obviously fail upon using
more avanced features of the respective formats.

Added
-----
- Support for entries in markdown format.
- Unit tests. Run with ``python3 -m unittest``

[0.3.1] - 2022-08-28
====================
Small bugfix; locking down version of parsedatetime to 2.5 . There have been
a couple of interface changes with the Calendar.parse method and this version
works so we're keeping it.

Fixed
-----
- parsedatetime locked to version 2.5

[0.3.0] - 2022-08-25
====================
Nothing major happend in this release, but I did modify an existing feature
in a backwards compaible way.

Added
-----
- Split out subparser subcommand functions.

Changed
-------
- Headings will no longer be auto sorted during output, nor will they be
  auto-upcased or down-cased. They will also no longer be automatically added
  to tags. Searching for headings remains case-insensitive though.
- The reason for the above change is that trying to create structure or order
  for a reasonably complicated daily entry was made impossible by the above
  "feature". So it was removed.

[0.2.0] - 2022-02-18
====================
This release adds the ability to perform batch additions / editing of entries,
fixes a couple of bugs, and changes the versioning of the project to use
single-source versioning. package.bash and setup.py will now determine the
version of daily from git-describe. Daily can now print its own version via
the ``--version`` option.

Added
-----
- Batch editing of entries.
- ``--version`` option to print the version of daily.
- Filter options to the "add" subcommand.
- Entries now display with an ID. This ID may not be searched on.

Changed
-------
- Version update methodology. Simply update the CHANGELOG with the new version
  when cutting a new release and then push a git tag named after that version.

Fixed
-----
- `daily show` not processing the `-d, --date` option.
- Bug in Journal.entry_filter function where providing only args.date
  would return all entries.
- Improper handling of `-d, --date` options in parsergroups.
- Package description in DEBIAN/control.

[0.1.0-alpha] - 2021-07-08
==========================
First release of "daily". There are a couple of known bugs and the features are
bare, but this release constitutes a minimal viable product as I envisioned
the program when I started. Each command has a functional "happy path", so
the program is operational.

Added
-----
- Installation and packaging logic for pywheel, deb, rpm, and gz.
- README for development instructions.
- General structure for manpages.
- General structure for unittests.
- Tab completion for all of daily (bash only).
- Basic configuration file and logic to fill in missing command-line args
  with those from the configuration file.
- Structure for argument parsing logic.
- pycodestyle configuration.
- Wrote man pages.
- Implemented the "add", "show", "refresh", and "upcoming" commands.
- Licensed under GPLv2.
