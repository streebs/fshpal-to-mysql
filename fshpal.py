from datetime import datetime
import sys

# this is a module that contains functtions that convert data imported from FSHPAL database to the indicated format

# will take a date in the format YYYYMMMDD and convert it to any format specified by the pattern parameter
def convertDate(input_date, output_pattern):
    try:
        input_date = datetime.strptime(input_date, '%Y%m%d')
    except ValueError as v:
        print(f'Incorrect date format used in fshpal.convertDate({input_date}), should be YYYYMMDD')
        raise v
    output_date_str = input_date.strftime(output_pattern)
    return output_date_str

# convert a date to seconds since the Unix epoch
def convertDateToSeconds(input_date):
    try:
        input_date = datetime.strptime(input_date, '%Y%m%d')
    except ValueError as v:
        print(f'Incorrect date format used in fshpal.convertDateToSeconds({input_date}), should be YYYYMMDD')
        raise v
    output_date = input_date.timestamp()
    return output_date

# convert a time stamp to HH:MM format. incoming format from FSHPAL is 0.HHMM
def convertTimeStamp(time_stamp):
    #remove the leading 0 from the time stamp
    # time_stamp = time_stamp[2:]

    try:
        time_stamp = datetime.strptime(time_stamp, '%H%M')
    except ValueError as v:
        print(f'Incorrect time format used in fshpal.convertTimeStamp({time_stamp}), should be HHMM')
        return v
    output_time_stamp = time_stamp.strftime('%H:%M')
    return output_time_stamp


print(convertTimeStamp(''))
