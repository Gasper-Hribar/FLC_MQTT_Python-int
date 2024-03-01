from typing import Type


list1 = [853,17469,0,0,0,0,0,0]
list2 = [bin(a) for a in list1]
list3 = []
def convert_read_val(readList):
    readList2 = [bin(a) for a in readList]
    readVals = [0,0,0,0,0,0,0,0]
    for a in readList2:
        a0 = a[2:]
        while len(a0) <= 15:
            a0 = '0' + a0
        if len(a0) == 16:
            a0 = '0b' + a0
        list3.append(a0)
    print(list3)
    for el in list3:
        if el != '0b0000000000000000':
            channelN = int(el[3:6], 2)
            readData = int(el[6:], 2)
            readVals[channelN] = readData
        else:
            pass
    return readVals

print(convert_read_val())


    # print(type(a))
    # slice = a[3:6]
    # res = int(slice)
    # print(res)


""" 
    p0c5s44444444
    p0c5w1cBv1
    p0c5s33333333
    p0r5 
"""