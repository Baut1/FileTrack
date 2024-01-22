def printAll(values):
    for row in values:
        print(row)

def printById(values, id):
    for row in values:
        if row[0] == id:
            print(row)