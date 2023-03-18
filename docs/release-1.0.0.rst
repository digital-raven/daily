Version 1.0.0 and breaking changes
==================================
Daily is now version 1.0.0! That said, There are breaking changes with how
entries are stored compared to version 0.4.0 . Daily now stores entries as
individual files in a directory, rather than compiling them into a json file.
This was done to be compatible with vimwiki.

If you were using the previous version and want to update, first dump your
current journal into a large text file using the old version of daily with

::

    daily show --before tomorrow > 2022-10-09.rst  # or md

And then manually update the entries there using some vim macros or sed or
something before using daily 1.0.0 to load that file. The individual entries
within should be written out to disk.

There shouldn't be any more breaking changes with the file format going foward.
If there are then the version of daily will update its major number to indicate
such a breaking change. Changes within the 1.x.x releases will be backwards
compatible with entry formats going forward.
