import pandas as pd
import sys
import datetime
import re
import os


def time_regex(str):
    p = re.compile('0?[1-9]|1[0-2]:[0-5][0-9]')
    return p.match(str)


def valid_date(datestring):
    try:
        mat = re.match('(\d{2})[/.-](\d{2})[/.-](\d{4})$', datestring)
        if mat is not None:
            t = datetime.datetime(*(map(int, mat.groups()[-1::-1])))
            return t
    except ValueError:
        pass
    return False


def validate_existence_of_data_dir():
    if not os.path.exists("sheets"):
        os.mkdir("sheets")


def validate_existence_of_monthly_csv(filename):
    if not os.path.exists(filename):
        return False
    return True


def extract_dataframe(filename):
    return pd.read_csv(filename)


def calculate_workTime(str1, str2):
    h1, m1 = int(str1.split(":")[0]), int(str1.split(":")[1])
    h2, m2 = int(str2.split(":")[0]), int(str2.split(":")[1])
    h = abs(h1 - h2)
    if h < 8:
        p = "30"
    else:
        p = "60"
    m = abs(m1 - m2)
    return str(h) + ":" + str(m), p


def main(start, end, date=datetime.date.today()):
    validate_existence_of_data_dir()
    filename = "sheets/" + str(date.month) + "_" + str(date.year) + '.csv'
    columns = ["Date", "Start", "End", "Total Time", "Break Time"]
    total, p = calculate_workTime(start, end)
    row = [[date, start, end, total, p + " mins"]]
    if validate_existence_of_monthly_csv(filename):
        tmp_df = pd.DataFrame(row, columns=columns)
        tmp_df.to_csv(filename, mode='a', index=False, sep=",", header=False)
        print(tmp_df)
    else:
        df = pd.DataFrame(row, columns=columns)
        df.to_csv(filename, index=False)


if __name__ == '__main__':
    if 2 < len(sys.argv) < 5:
        if time_regex(sys.argv[1]) and time_regex(sys.argv[2]):
            start = sys.argv[1]
            end = sys.argv[2]
            if len(sys.argv) == 4:
                day = valid_date(sys.argv[3])
                if day:
                    main(start, end, day)
            else:
                main(start, end)
        else:
            start = sys.argv[1]
            end = sys.argv[2]
            print(start, end)
            print("Error Time Format")
    else:
        print("python3 [start time] [end time] [options ..] "
              "options : mm-dd-yyyy")
