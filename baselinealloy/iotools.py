import re
import csv


def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    try : # python 2/3 string differences
        column = column.decode('utf8')
    except AttributeError:
        pass
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column

def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            #print(clean_row)
            row_id = int(row['ID'])
            data_d[row_id] = dict(clean_row)

    return data_d

def storePreProcessedData(data_d):
    with open('abtbuy3196processed.csv','w',newline='') as  cf:
        csvhead = ['ID','Entity_id','unique_id','textual']  # write head
        writer = csv.DictWriter(cf,fieldnames=csvhead)
        writer.writeheader();
        for record in data_d.values():
            writer.writerow(record)
