def get_epoch_minute(datetime):
    """Takes a datetime and strips seconds/microseconds and
    converts to an epoch timestamp

    Args:
        datetime (datetime): datetime to convert
    """
 
    truncated = datetime.replace(second=0, microsecond=0)
    return truncated.strftime('%s')
