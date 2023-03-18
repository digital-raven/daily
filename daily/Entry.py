import hashlib
import json
import re
from datetime import datetime


# Find heading points.
def _is_rst_heading(s):
    s = s.strip()
    return (s.startswith('=') and s.endswith('=')
            or s.startswith('-') and s.endswith('-'))


def _is_md_heading(s):
    s = s.strip()
    return s.startswith('# ') or s.startswith('## ')


def _get_headings_and_text(rst):
    """ Separate out top-level headings and text.
    """
    headings = []
    text = []

    split = re.split('=+\n', rst)
    split = [s.splitlines() for s in split]

    headings.append(split[0][0])

    for body in split[1:-1]:
        text.append('\n'.join(body[:-1]))
        headings.append(body[-1])

    text.append('\n'.join(split[-1]))

    return headings, text


def get_entries_from_md(md):
    """ Parse many entries out of markdown text.
    """
    if not md.strip():
        return []

    # Markdown entries are terminated by a line containing only this string.
    end_str = '<!--- End Daily Entry --->'
    texts = md.split(end_str)[:-1]
    entries = []

    for t in texts:
        entries.append(Entry.createFromMd('\n'.join([t.strip(), end_str])))

    return entries


def get_entries_from_rst(rst):
    if not rst.strip():
        return []

    entries = []
    titles, contents = _get_headings_and_text(rst)

    for t, c in zip(titles, contents):
        entries.append(Entry.createFromRst('\n'.join([t, '===', c])))

    return entries


def _gen_id(title):
    dt = datetime.today()
    s = '{}-{}-{}_{}-{}-{}-{}'.format(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond)
    h = hashlib.sha1()
    h.update(bytes(title + s, 'utf-8'))
    return h.hexdigest() + '-' + s


class Entry:
    """ Represents a single entry from a journal.
    """
    def __init__(self, title, headings, tags, id_=None):
        """ Create a new entry.

        Args:
            title: Title of the entry.
            headings: Dictionary of subheadings. Each heading is paired with
                a string for its entry.
            tags: Set of tags for the entry at large.
            id_: The entry's unique ID. If None, then one will be generated.
                If this is provided, ensure it is unique.
        """
        self.title = title
        self.headings = {k: v for k, v in headings.items()}
        self.tags = tags
        self.id = id_
        if not self.id:
            self.id = _gen_id(title)

        self.refresh()

    def addHeadings(self, headings):
        """ Add new headings to the entry.

        Args:
            headings: List of headings to add. No content will be added.
        """
        headings = [x for x in headings]
        for heading in headings:
            if heading not in self.headings:
                self.headings[heading] = ''

        self.refresh()

    @classmethod
    def createBlankEntry(cls, title):
        """ Create a blank entry. Still needs a title.

        Args:
            title: Title of the entry.
        """
        return Entry(title, dict(), [])

    @classmethod
    def fromDict(cls, d):
        """ Init an entry from a dict.

        Args:
            d: The dict to create the entry from. Needs to have "title",
                "headings", and a "tags" field per the Entry.__init__ method.

        Returns:
            A new Entry.

        Raises:
            ValueError if d doesn't contain the expected fields.
        """
        try:
            id_ = d['id'] if 'id' in d else None
            return Entry(d['title'], d['headings'], d['tags'], id_)
        except KeyError as ke:
            raise ValueError('Missing "title", "headings" or "tags" fields.')

    @classmethod
    def createFromMd(cls, md):
        """ Create a new Entry from markdown text.

        The text will be parsed to derive key-value entries where the key
        is the heading and the value is the subsequent text.

        The title of the entry is expected to be a markdown level-1 heading
        (# ) This is followed by the entry's notes, which is then
        succeeded by the rest of the entry's headings, which are expected
        to be RST level 2 headings (## ).

        Args:
            md: Markdown text from which to create the entry.

        Returns:
            A new Entry.

        Raises:
            ValueError if the markdown could not create a valid Entry.
        """
        md = md.strip().splitlines()

        if not md:
            raise ValueError('The entry was empty.')

        ptr = 0

        title = ''
        headings = {}
        tags = []

        # Strip off ending string.
        if md[-1] == '<!--- End Daily Entry --->':
            md = md[:-1]

        # Tags should be on the last line.
        if md[-1].strip().startswith('tags:'):
            tags = md[-1].replace(',', ' ').replace(':', ' ').split()[1:]
            tags = sorted(list(set(tags)))
            md = md[:-1]

        # ID should be on the second to last line. An ID will be generated if
        # not present.
        id_ = None
        md = '\n'.join(md).strip().splitlines()
        if md[-1].strip().startswith('id:'):
            id_ = md[-1].replace(':', ' ').split()[1]
            md = md[:-1]

        # Find the headings and content.
        heading_pts = [x for x, y in enumerate(md) if _is_md_heading(y)]

        # Find the title.
        if not heading_pts:
            raise ValueError('No title in entry.')

        heading_pts.append(len(md))

        title = ' '.join(md[heading_pts[0]].split()[1:])

        # Gather notes
        headings['notes'] = '\n'.join(md[1:heading_pts[1]])

        # ... and delete the "notes" entry if no notes were entered.
        if not headings['notes'].strip():
            del(headings['notes'])

        # Get the rest
        for ptr in range(1, len(heading_pts) - 1):
            heading = ''.join(md[heading_pts[ptr]].split('##')[1:]).strip()
            content_start = heading_pts[ptr] + 1
            content_end = heading_pts[ptr + 1]
            headings[heading] = '\n'.join(md[content_start:content_end])

        return Entry(title, headings, tags, id_)

    @classmethod
    def createFromRst(cls, rst):
        """ Create a new Entry from RST text.

        The RST will be parsed to derive key-value entries where the key
        is the heading and the value is the subsequent text.

        The title of the entry is expected to be an RST level-1 heading
        (=====). This is followed by the entry's notes, which is then
        succeeded by the rest of the entry's headings, which are expected
        to be RST level 2 headings (-----).

        Args:
            rst: RST-formatted text from which to create the entry.

        Returns:
            A new Entry.

        Raises:
            ValueError if the RST could not create a valid Entry.
        """
        rst = rst.strip().splitlines()

        if not rst:
            raise ValueError('The entry was completely empty.')

        ptr = 0

        title = ''
        headings = {}
        tags = []

        # Extract the tags first, if present. They should be on the last line.
        if rst[-1].strip().startswith('tags:'):
            tags = rst[-1].replace(',', ' ').replace(':', ' ').split()[1:]
            tags = sorted(list(set(tags)))
            rst = rst[:-1]

        # ID should be on the second to last line. An ID will be generated if
        # not present.
        id_ = None
        rst = '\n'.join(rst).strip().splitlines()
        if rst[-1].strip().startswith('id:'):
            id_ = rst[-1].replace(':', ' ').split()[1]
            rst = rst[:-1]

        # Find the headings and content.
        heading_pts = [x - 1 for x, y in enumerate(rst) if _is_rst_heading(y)]

        # Find the title.
        if not heading_pts or heading_pts[0] == -1:
            raise ValueError('No title in entry.')

        heading_pts.append(len(rst))

        title = rst[heading_pts[0]]

        # Gather notes
        headings['notes'] = '\n'.join(rst[heading_pts[0] + 2:heading_pts[1]])

        # ... and delete the "notes" entry if no notes were entered.
        if not headings['notes'].strip():
            del(headings['notes'])

        # Get the rest
        for ptr in range(1, len(heading_pts) - 1):
            heading = rst[heading_pts[ptr]]
            content_start = heading_pts[ptr] + 2
            content_end = heading_pts[ptr + 1]
            headings[heading] = '\n'.join(rst[content_start:content_end])

        return Entry(title, headings, tags, id_)

    def refresh(self):
        """ Refresh tags and headings.

        Tags should be sorted.
        """
        self.tags = sorted(list(set([x for x in self.tags])))

    def update(self, new_entry, exp_headings=None):
        """ Update an entry.

        The title and tags of this entry will be replaced, and new
        headings will be added, while any headings which were expected
        to be in the new entry (but weren't) will be deleted from this
        entry.

        Args:
            new_entry: Other entry instance whose values will be used.
            exp_headings: If a heading is listed here, but is not found in
                rst, then the heading will be deleted from the entry.

        Raises:
            See createFromRst.
        """
        exp_headings = exp_headings or []

        # Update this entry.
        self.title = new_entry.title
        self.tags = new_entry.tags

        if not exp_headings:
            self.headings = new_entry.headings
        else:
            for heading in exp_headings:
                if heading not in new_entry.headings and heading in self.headings:
                    del(self.headings[heading])

            self.headings.update(new_entry.headings)

        self.refresh()

    def getMd(self, headings=None, force=False):
        display = False

        headings = headings or []
        headings = headings or self.headings
        headings = [x.lower() for x in headings]

        s = []
        s.append('# ' + self.title)

        if 'notes' in headings:
            display = True
            s.append(self.headings['notes'])

        # case-insensitive search
        lookup_headings = {k.lower(): k for k in self.headings}
        for heading in headings:
            if heading == 'notes' or heading not in lookup_headings:
                continue

            display = True
            s.append('## ' + lookup_headings[heading])
            s.append(self.headings[lookup_headings[heading]])

        # No content, but add an empty line for good-looks
        if not display and force:
            s.append('')

        s.append('id: ' + self.id)
        s.append('tags: ' + ' '.join(self.tags))
        s.append('<!--- End Daily Entry --->')

        # Will become trailing newline
        s.append('')
        s.append('')

        if display or force:
            return '\n'.join(s)
        else:
            return ''

    def getRst(self, headings=None, force=False):
        """ Display this entry in RST format.

        Args:
            headings: Only show the listed headings. Will show all
                headings if this value is None.
            force: Force the display even if there is no content.

        Returns:
            An RST string representing the content of this entry.

        Raises:
            KeyError if a heading wasn't in self.headings.
        """
        display = False

        headings = headings or []
        headings = headings or self.headings
        headings = [x.lower() for x in headings]

        s = []
        s.append(self.title)
        s.append('=' * len(self.title))

        if 'notes' in headings:
            display = True
            s.append(self.headings['notes'])

        # case-insensitive search
        lookup_headings = {k.lower(): k for k in self.headings}
        for heading in headings:
            if heading == 'notes' or heading not in lookup_headings:
                continue

            display = True
            s.append(lookup_headings[heading])
            s.append('-' * len(lookup_headings[heading]))
            s.append(self.headings[lookup_headings[heading]])

        # No content, but add an empty line for good-looks
        if not display and force:
            s.append('')

        s.append('id: ' + self.id)
        s.append('tags: ' + ' '.join(self.tags))

        # Will become trailing newline
        s.append('')

        if display or force:
            return '\n'.join(s)
        else:
            return ''

    def __eq__(self, o):
        return self.title == o.title

    def __lt__(self, o):
        return self.title.lower() < o.title.lower()
