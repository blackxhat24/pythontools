SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def main():
    myMessage = """"Encryption works. Properly implemented strong crypto systems are one of the few things
that you can rely on. Unfortunately, endpoint security is so terrifically weak that NSA can
frequently find ways around it." ― Edward Snowden"""
    myKey = 'DUMPLINGS'
    print(f'Vigenere Key: {myKey}')
    print('')
    Encryption = EncryptMessage(myKey, myMessage)
    Decryption = DecryptMessage(myKey, Encryption)
    print('Vigenere ciphertext:')
    print(Encryption)
    print('')
    print('Vigenere plaintext:')
    print(Decryption)


def EncryptMessage(key, message):
    translated = []
    
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = SYMBOLS.find(symbol.upper())
        if num != -1:
            num += SYMBOLS.find(key[keyIndex])
            num %= len(SYMBOLS)
            if symbol.isupper():
                translated.append(SYMBOLS[num])
            elif symbol.islower():
                translated.append(SYMBOLS[num].lower())
            
            keyIndex += 1
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)

    return ''.join(translated)

def DecryptMessage(key, message):
    translated = []
    
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = SYMBOLS.find(symbol.upper())
        if num != -1:
            num -= SYMBOLS.find(key[keyIndex])
            if symbol.isupper():
                translated.append(SYMBOLS[num])
            elif symbol.islower():
                translated.append(SYMBOLS[num].lower())
            
            keyIndex += 1
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)

    return ''.join(translated)


if __name__ == '__main__':
    main()