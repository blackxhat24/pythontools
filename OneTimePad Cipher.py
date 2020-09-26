import secrets
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def generateOtp(message):
    otp = ''
    for i in range(len(message)):
        otp += secrets.choice(SYMBOLS)
    
    print('One Time Pad Key:')
    print(otp.upper())
    return otp

def main():
    myMessage = """"Encryption works. Properly implemented strong crypto systems are one of the few things
that you can rely on. Unfortunately, endpoint security is so terrifically weak that NSA can
frequently find ways around it." ― Edward Snowden"""

    myKey = generateOtp(myMessage)
    print('')
    Encryption = EncryptMessage(myKey, myMessage)
    Decryption = DecryptMessage(myKey, Encryption)
    print('One Time Pad ciphertext:')
    print(Encryption)
    print('')
    print('One Time Pad plaintext:')
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


if __name__ == '__main__':
    main()