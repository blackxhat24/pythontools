import math

message = 'Cenoonommstmme oo snnio. s s c'

key = 8

def decryptMessage(key, message):
    numOfColumns = int(math.ceil(len(message) / float(key)))
    numOfRows = key
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
    plaintext = [''] * numOfColumns

    column = 0
    row = 0

    for symbol in message:
        plaintext[column] += symbol
        column += 1

        if(column == numOfColumns) or (column == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            column = 0
            row += 1
    return ''.join(plaintext)

plaintext = decryptMessage(key,message)
print(plaintext)