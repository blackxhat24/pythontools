SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def encryption():
    print("Encryption")

    print("Message can only be lower or uppercase alphabet")
    msg = input("Enter Message: ")
    key = int(input("Enter Key(0-25): "))

    translated = ""
    for symbol in msg:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = (symbolIndex + key) % 66
            translated = translated + SYMBOLS[translatedIndex]
        else:
            translated = translated + symbol
    print(f"Encrypted: {translated}")
    input()

def decryption():
    print("Decryption")
    print("Message can only be lower or uppercase alphabet")
    cipher = input("Enter encrypted text: ")
    cipherkey = int(input("Enter key(0-25): "))
    translated = ""
    for symbol in cipher:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = (symbolIndex - cipherkey) % 66
            translated = translated + SYMBOLS[translatedIndex]
        else:
            translated = translated + symbol
    print(f"Decrypted Text: {translated}")
    input()

def main():
    choice = int(input("1. Encryption\n2. Decryption\nChoose:"))
    if choice == 1:
        encryption()
    elif choice == 2:
        decryption()
    else:
        print("Wrong Choice")

if __name__ == "__main__":
    main()
