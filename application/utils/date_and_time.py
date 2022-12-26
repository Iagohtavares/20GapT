import datetime


def formated(entry_datetime=None, entry_format=None):
    if entry_datetime in ["now"] and entry_format in ['timestamp']:
        entry_datetime = datetime.datetime.now()
        return int(entry_datetime.timestamp())

    elif entry_datetime in ["now"] and entry_format in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]:
        entry_datetime = datetime.datetime.now()
        return entry_datetime.strftime(entry_format)

    elif entry_datetime in ["now"] and not entry_format:
        return datetime.datetime.now()

    else:
        pass


    if entry_datetime in ["today"] and entry_format in ['timestamp']:
        entry_datetime = datetime.datetime.today()
        return int(entry_datetime.timestamp())

    elif entry_datetime in ["today"] and entry_format in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]:
        entry_datetime = datetime.datetime.today()
        return entry_datetime.strftime(entry_format)

    elif entry_datetime in ["today"] and not entry_format:
        return datetime.datetime.today()

    else:
        pass


    if isinstance(entry_datetime, str) and entry_format in ['timestamp']:
        try:
            return int(datetime.datetime.strptime(entry_datetime, "%d/%m/%Y %H:%M:%S").timestamp())
        except:
            return int(datetime.datetime.strptime(entry_datetime, "%d/%m/%Y").timestamp())

    else:
        datetime_form = entry_datetime


    if isinstance(entry_datetime, int) and entry_format in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]:
        entry_datetime = datetime.datetime.fromtimestamp(entry_datetime)
        return entry_datetime.strftime(entry_format)

    elif isinstance(entry_datetime, int) and entry_format in ["datetime"]:
        return datetime.datetime.fromtimestamp(entry_datetime)

    else:
        datetime_form = entry_datetime


    if isinstance(entry_datetime, datetime.datetime) and entry_format in ['timestamp']:
        return int(entry_datetime.timestamp())

    elif isinstance(entry_datetime, datetime.datetime) and entry_format in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]:
        return entry_datetime.strftime(entry_format)

    else:
        datetime_form = entry_datetime

    return datetime_form
