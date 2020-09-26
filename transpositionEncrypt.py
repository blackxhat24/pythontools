message = 'Common sense is not so common.'

key = 8

def encryptMessage(key,message):
    ciphertext = [''] * key
    for column in range(key):
        currentIndex = column

        while currentIndex < len(message):
            ciphertext[column] += message[currentIndex]
            currentIndex += key

    return ''.join(ciphertext)

cipher = encryptMessage(key,message)
print(cipher)
 
