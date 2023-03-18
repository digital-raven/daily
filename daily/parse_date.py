from datetime import date, datetime, timedelta

import parsedatetime as pdt


def get_title_from_date(date, format_='%Y-%m-%d, %a'):
    """ Generate a more human-readable title.

    Returns:
        A string showing the date in Y-m-d format and the weekday.

    Raises:
        ValueError if date could not be parsed.
    """
    return parse_date(date).strftime(format_)


def parse_date(date_, _cache={}):
    """ Parse a str into a date or datetime.

    If a time is parsed then it will have precision down to the minute.

    Args:
        date_: Date to parse.
        _cache: Do not touch. This caches requests and will clear if
            it has been longer than a minute since the previous call.

    Returns:
        A date or datetime object.

    Raises:
        ValueError if date could not be parsed.
    """
    if type(date_) in [date, datetime]:
        return date_
    date_ = str(date_)

    # Init cache. It clears if the minute has changed since the previous call.
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute)

    if '__init' not in _cache or now != _cache['__init']:
        _cache.clear()
        _cache['__init'] = now

    if date_ in _cache:
        return _cache[date_]

    fmts = [
        '%Y-%m-%d, %a',
        '%Y-%m-%d',
    ]

    for fmt in fmts:
        try:
            _cache[date_] = datetime.strptime(date_, fmt).date()
            return _cache[date_]
        except ValueError:
            pass

    # Maybe it contains a time element
    try:
        _cache[date_] = datetime.strptime(date_, '%Y-%m-%d, %a, %H:%M')
        return _cache[date_]
    except ValueError:
        pass

    # Didn't match any clean format. Time for the parser.
    cal = pdt.Calendar(version=pdt.VERSION_FLAG_STYLE)
    d, flag = cal.parse(date_)

    if not flag:
        raise ValueError(f'The date "{date_}" could not be parsed.')

    # flag is 1 for date, 2 for time, 3 for datetime
    if flag == 1:
        _cache[date_] = date(*d[:3])
    else:
        _cache[date_] = datetime(*d[:5])

    return _cache[date_]


def parse_duration(duration):
    """ Return a timedelta from a duration str.

    Can handle humanized durations. Like "40min" or "1 hour". Handles
    down to minute precision.

    Args:
        duration: Duration to turn into timedelta.

    Returns:
        timedelta object.
    """
    if type(duration) is timedelta:
        return duration

    later = parse_date(duration)
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute)

    return later - now
