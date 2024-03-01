MCPdig = 4096
binary = bin(MCPdig)
# print(len(binary))
# bin1 = binary[2:]
# listek = []
# for val in bin1[::-1]:
#     print(val)

def sortDIGvals(val, chiptype):
    listDIG = []
    bin0 = bin(val)
    bin1 = bin0[2:]
    for val in bin1[::-1]:
        listDIG.append(int(val))
    if chiptype == 'mcp':
        while len(listDIG) < 16:
            listDIG.append(0)
    elif chiptype == 'add':
        while len(listDIG) < 8:
            listDIG.append(0)
    else:
        print('Wrong chiptype')
    return listDIG
sortDIGvals(MCPdig, 'mcp')