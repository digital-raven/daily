import sys

from daily.Journal import Journal

def do_refresh(args):
    old = Journal()
    new = Journal()

    old.load(args.journal)

    for entry in old:
        try:
            new[entry.title] = entry
        except ValueError as ve:
            print('ERROR: {}'.format(ve))
            sys.exit(1)

    new.write(args.journal)
