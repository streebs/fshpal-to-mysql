import sys
import pandas as pd
from datetime import datetime
import pytz
import test

def addDash(s):
    return s[:4] + '-' + s[4:6] + '-' + s[6:]

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
    # df['date'] = df['date'].map(lambda x: addDash(str(x)))
    df['date'] = df['date'].map(lambda x: toUTC(str(x)))

    # convert the timei column to 24 hour format
    df['timei'] = df['timei'].map(lambda x: str(x)[2:])
    df['timei'] = df['timei'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

    # convert the timei column to 24 hour format
    df['timeo'] = df['timeo'].map(lambda x: str(x)[2:])
    df['timeo'] = df['timeo'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

    # convert the timev column to HH:MM format
    df['timev'] = df['timev'].map(lambda x: str(x)[2:])
    df['timev'] = df['timev'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

    #test the data
    errNum = 0
    rowList = []
    for index, row in df.iterrows():
        if not test.test_date(str(row['date'])):
            print('Error on row ' + str(index) + ' date value ' + str(row['date']))
            rowList.append(index)
            errNum += 1
        if not test.test_times(str(row['timei'])):
            print('Error on row ' + str(index) + ' timei value ' + str(row['timei']))
            rowList.append(index)
            errNum += 1
        if not test.test_times(str(row['timeo'])):
            print('Error on row ' + str(index) + ' timeo value ' + str(row['timeo']))
            rowList.append(index)
            errNum += 1
        if not test.test_times(str(row['timev'])):
            print('Error on row ' + str(index) + ' timev value ' + str(row['timev']))
            rowList.append(index)
            errNum += 1
        if not test.test_uvid(str(row['uvid'])):
            print('Error on row ' + str(index) + ' uvid value ' + str(row['uvid']))
            rowList.append(index)
            errNum += 1
        if not test.test_name(str(row['name'])):
            print('Error on row ' + str(index) + ' name value ' + str(row['name']))
            rowList.append(index)
            errNum += 1
        if not test.test_center(str(row['center'])):
            print('Error on row ' + str(index) + ' center value ' + str(row['center']))
            rowList.append(index)
            errNum += 1
        if not test.test_class(str(row['class'])):
            print('Error on row ' + str(index) + ' class value ' + str(row['class']))
            rowList.append(index)
            errNum += 1

    # write the dataframe to a csv file if there are no errors
    if errNum == 0:
        df.to_csv(outputfile, index=False)
    else:
        i = input('There were ' + str(errNum) + ' errors. would you like to remove them? (y/n)')
        df.drop(df.index[rowList], inplace=True) if i == 'y' else print('No changes made.')
        df.to_csv(outputfile, index=False) if i == 'y' else print('No output file created.')
        print('Finished')



if __name__ == '__main__':
    main()