def datetimeToStr(dateTime):
    year = str(dateTime.year)
    month = str(dateTime.month)
    day = str(dateTime.day)
    return year + "-" + month + "-" + day


def v2Q(v):
    return "\"" + v + "\""
