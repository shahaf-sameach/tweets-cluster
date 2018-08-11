import datetime


def custom_converter(o):
    """Custom converter for datatime"""
    if isinstance(o, datetime.datetime):
        return o.__str__()

