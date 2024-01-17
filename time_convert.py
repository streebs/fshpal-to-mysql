from datetime import datetime
import pytz


def toUTC(s):
    # Define the input date and time in MDT
    mdt_time = s  # Replace this with your MDT time

    # Create a datetime object with MDT timezone
    mdt_timezone = pytz.timezone("US/Mountain")
    mdt_datetime = mdt_timezone.localize(datetime.strptime(mdt_time, "%Y%m%d"))

    # Convert the MDT datetime to UTC
    utc_datetime = mdt_datetime.astimezone(pytz.UTC)

    # Convert the UTC datetime to seconds since the Unix epoch
    utc_seconds = (utc_datetime - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return int(utc_seconds)