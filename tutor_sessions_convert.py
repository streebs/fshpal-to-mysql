import sys
import pandas as pd
import test
import spinner
import time_convert as tc


def main():
    inputfile = ''
    outputfile = ''
    flag = sys.argv[1]

    if flag == '-t' and len(sys.argv) != 3:
        print('Usage: python tutor-visits-convert.py -t <testfile>')
        sys.exit(1)
    
    if flag == '-o' and len(sys.argv) != 4:
        print('Usage: python tutor-visits-convert.py -o <inputfile> <outputfile>')
        sys.exit(1)

    inputfile = sys.argv[2]

    outputfile = sys.argv[3] if len(sys.argv) == 4 else sys.exit(1)

    dtype={'tutor_id': 'Int64'}

    index = ["record_id", "visit_id", "date", "timei", "times", "timeo", "timev", "reason", "tutor_id"]
    df = pd.read_csv(inputfile, dtype=dtype)

    # removing columns that are not needed. This is because the tutor_visits table in the database already has these columns
    # drop the following columns: student_id, student_name, center, class, visit_type
    df.drop(df.columns[[7,8,9,10,11,14]], axis=1, inplace=True)

    df.columns = index

    # DATA CLEANING
    # convert to numeric and drop rows that are not numeric, finally convert to integers.
    df['tutor_id'] = pd.to_numeric(df['tutor_id'], errors='coerce', downcast='integer')
    df.dropna(subset=['tutor_id'], inplace=True)
    df['tutor_id'] = df['tutor_id'].astype(int)

    
    if flag == '-t':
        for index, row in df.iterrows():
            if len(str(row['timei'])) != 6:
                print('Error on row ' + str(index) + ' timei value ' + str(row['timei']))
            if len(str(row['timeo'])) != 6:
                print('Error on row ' + str(index) + ' timeo value ' + str(row['timeo']))
        sys.exit(1)

    with spinner.Spinner("converting data... "):

        df['date'] = df['date'].map(lambda x: tc.toUTC(str(x)))

        df['timei'] = df['timei'].map(lambda x: str(x)[2:])
        df['timei'] = df['timei'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

        df['timeo'] = df['timeo'].map(lambda x: str(x)[2:])
        df['timeo'] = df['timeo'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

        df['times'] = df['times'].map(lambda x: str(x)[2:])
        df['times'] = df['times'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

        df['timev'] = df['timev'].map(lambda x: str(x)[2:])
        df['timev'] = df['timev'].map(lambda x: x[:2] + ':' + x[2:] if len(str(x)) == 4 else x[:2] + ':' + x[2:] + '0' if len(str(x)) == 3 else x[:2] + ':' + x[2:] + '0' + '0' if len(str(x)) == 2 else x[:1] + '0:00')

        

        errNum = 0
        rowList = []
        errors = []
    with spinner.Spinner("testing data conversions... "):
        for index, row in df.iterrows():
            if not test.test_date(str(row['date'])):
                errors.append('Error on row ' + str(index) + ' date value ' + str(row['date']))
                rowList.append(index)
                errNum += 1
            if not test.test_times(str(row['timei'])):
                errors.append('Error on row ' + str(index) + ' timei value ' + str(row['timei']))
                rowList.append(index)
                errNum += 1
            if not test.test_times(str(row['timeo'])):
                errors.append('Error on row ' + str(index) + ' timeo value ' + str(row['timeo']))
                rowList.append(index)
                errNum += 1
            if not test.test_times(str(row['times'])):
                errors.append('Error on row ' + str(index) + ' times value ' + str(row['times']))
                rowList.append(index)
                errNum += 1
            if not test.test_times(str(row['timev'])):
                errors.append('Error on row ' + str(index) + ' timev value ' + str(row['timev']))
                rowList.append(index)
                errNum += 1
            if not test.test_reason(str(row['reason'])):
                errors.append('Error on row ' + str(index) + ' reason value ' + str(row['reason']))
                rowList.append(index)
                errNum += 1
            if not test.test_uvid(str(row['tutor_id'])):
                errors.append('Error on row ' + str(index) + ' tutor_id value ' + str(row['tutor_id']))
                rowList.append(index)
                errNum += 1

    if errNum == 0:
        print('No errors found. Writing converted data to ' + outputfile)
        df.to_csv(outputfile, index=False)
    else:
        for e in errors:
            print(e)
        print('There were ' + str(errNum) + ' errors. Would you like to remove them? (y/n)')
        i = input()
        if i == 'y':
            for i in rowList:
                if i in df.index:
                    df.drop(i, inplace=True)
                
            df.to_csv(outputfile, index=False)
            print('Items removed. Writing converted data to ' + outputfile)
        else:
            df.to_csv(outputfile, index=False)
            print('No changes made. Writing converted data to ' + outputfile + ' with errors')
            
    print('Done!')


if __name__ == "__main__":
    main()