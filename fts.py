import sys
import pandas as pd
from datetime import datetime
import pytz

def addDash(s):
    return s[:4] + '-' + s[4:6] + '-' + s[6:]

def toUTC(s):
    # Define the input date and time in MDT
    mdt_time = s  # Replace this with your MDT time

    # Create a datetime object with MDT timezone
    mdt_timezone = pytz.timezone("US/Mountain")
    mdt_datetime = mdt_timezone.localize(datetime.strptime(mdt_time, "%Y-%m-%d"))

    # Convert the MDT datetime to UTC
    utc_datetime = mdt_datetime.astimezone(pytz.UTC)

    # Convert the UTC datetime to seconds since the Unix epoch
    utc_seconds = (utc_datetime - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return int(utc_seconds)



def main():
    
    inputfile = ''
    outputfile = ''

    if sys.argv[1] == '-t' and len(sys.argv) != 3:
        print('Usage: python fts.py -t <testfile>')
        sys.exit(1)
    
    if sys.argv[1] == '-o' and len(sys.argv) != 4:
        print('Usage: python fts.py <inputfile> <outputfile>')
        sys.exit(1)

    inputfile = sys.argv[2]

    outputfile = sys.argv[3] if len(sys.argv) == 4 else sys.exit(1)

    index=['record_id', 'date', 'timei', 'timeo', 'timev', 'uvid', 'name', 'center', 'class']

    # read csv file and rename columns. for some reason the FSHPAL csv file has extra whitespace in the column names
    df = pd.read_csv(inputfile)
    df.columns = index

    # convert the date column to YYYY-MM-DD format then convert to UTC in seconds since epoch
    df['date'] = df['date'].map(lambda x: addDash(str(x)))
    df['date'] = df['date'].map(lambda x: toUTC(str(x)))

    # convert the timei column to HH:MM format
    df['timei'] = df['timei'].map(lambda x: str(x)[2:])
    df['timei'] = df['timei'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

    df.to_csv(outputfile, index=False)


if __name__ == '__main__':
    main()