import json


def encryptCharReflector(reflectorDict, encryptedChar):

    return reflectorDict[encryptedChar]


def encryptCharRotorOut(rotor, ringSet, ringPos, encryptedChar):
    newRotor = ''
    ringSet = ord(ringSet)-65
    if ringSet != 0:
        i = 26 - ringSet + 1
        newRotor += chr((ord(rotor[26 - ringSet]) - 65 + ringSet) % 26 + 65)
        while i != len(rotor) - ringSet:
            i %= 26
            newRotor += chr((ord(rotor[i]) - 65 + ringSet) % 26 + 65)
            i += 1
    else:
        newRotor += rotor

    cipherNum = chr((((ord(encryptedChar) - 65) + (ord(ringPos) - 65)) % 26) + 65)

    encryptedChar = chr((((newRotor.index(cipherNum)) - (ord(ringPos) - 65) + 26) % 26) + 65)

    return encryptedChar


def encryptCharRotorIn(rotor, ringSet, ringPos, encryptedChar):
    newRotor = ''
    ringSet = ord(ringSet)-65
    if ringSet != 0:
        i = 26 - ringSet + 1
        newRotor += chr((ord(rotor[26 - ringSet]) - 65 + ringSet) % 26 + 65)
        while i != len(rotor) - ringSet:
            i %= 26
            newRotor += chr((ord(rotor[i]) - 65 + ringSet) % 26 + 65)
            i += 1
    else:
        newRotor += rotor

    cipherNum = ord(newRotor[((ord(encryptedChar) - 65) + (ord(ringPos) - 65)) % 26]) - 65

    encryptedChar = chr(((cipherNum - (ord(ringPos) - 65) + 26) % 26) + 65)

    return encryptedChar


def encryptText(codeBookDict, rotorsDict, reflectorDict, day, text):
    text = text.upper()
    encryptedText = ''
    i = 2
    j = 0
    for char in text:
        if char > 'Z' or char < 'A':
            if ord(char) > 57 or ord(char) < 48:
                text = text.replace(char, '')

    positions = codeBookDict[day]["positions"]

    for letter in text:
        if 'A' <= letter <= 'Z':
            if positions[1] == rotorsDict[codeBookDict[day]["rotors"][1]]["notch"] or (
                    positions[1] == rotorsDict[codeBookDict[day]["rotors"][1]]["notch"] and positions[2] ==
                    rotorsDict[codeBookDict[day]["rotors"][2]]["notch"]):

                if positions[0] == 'Z':
                    positions = positions.replace(positions[0], chr((ord(positions[0]) - 25)), 1)
                else:
                    positions = positions.replace(positions[0], chr((ord(positions[0]) + 1)), 1)

                if positions[1] == 'Z' and positions[1] != positions[0]:
                    positions = positions.replace(positions[1], chr((ord(positions[1]) - 25)), 1)
                elif positions[1] == positions[0] and positions[1] != 'Z':
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 2)
                    positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
                elif positions[1] == positions[0] and positions[1] == 'Z':
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 2)
                    positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
                else:
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 1)

            elif positions[2] == rotorsDict[codeBookDict[day]["rotors"][2]]["notch"]:

                if positions[1] == 'Z' and positions[1] != positions[0]:
                    positions = positions.replace(positions[1], chr((ord(positions[1]) - 25)), 1)
                elif positions[1] == positions[0] and positions[1] != 'Z':
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 2)
                    positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
                elif positions[1] == positions[0] and positions[1] == 'Z':
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 2)
                    positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
                else:
                    positions = positions.replace(positions[1], chr((ord(positions[1]) + 1)), 1)

            if positions[2] == 'Z' and positions[1] == 'Z' and positions[0] == 'Z':
                positions = positions.replace(positions[2], chr((ord(positions[2]) - 25)), 3)
                positions = positions.replace(positions[0], chr((ord(positions[0]) + 25)), 1)
                positions = positions.replace(positions[1], chr((ord(positions[1]) + 25)), 1)
            elif positions[2] == 'Z' and positions[1] == 'Z':
                positions = positions.replace(positions[2], chr((ord(positions[2]) - 25)), 2)
                positions = positions.replace(positions[1], chr((ord(positions[1]) + 25)), 1)
            elif positions[2] == 'Z' and positions[0] == 'Z':
                positions = positions.replace(positions[2], chr((ord(positions[2]) - 25)), 2)
                positions = positions.replace(positions[0], chr((ord(positions[0]) + 25)), 1)
            elif positions[2] == 'Z':
                positions = positions.replace(positions[2], chr((ord(positions[2]) - 25)), 1)
            elif positions[2] == positions[1] and positions[2] == positions[0]:
                positions = positions.replace(positions[2], chr((ord(positions[2]) + 1)), 3)
                positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
                positions = positions.replace(positions[1], chr((ord(positions[1]) - 1)), 1)
            elif positions[2] == positions[1]:
                positions = positions.replace(positions[2], chr((ord(positions[2]) + 1)), 2)
                positions = positions.replace(positions[1], chr((ord(positions[1]) - 1)), 1)
            elif positions[2] == positions[0]:
                positions = positions.replace(positions[2], chr((ord(positions[2]) + 1)), 2)
                positions = positions.replace(positions[0], chr((ord(positions[0]) - 1)), 1)
            else:
                positions = positions.replace(positions[2], chr((ord(positions[2]) + 1)), 1)

            encryptedChar = letter
            for encryption in range(0, 3):
                setting = codeBookDict[day]["settings"]
                setting = setting[i]
                position = positions[i]
                rotor = codeBookDict[day]["rotors"]
                rotor = rotor[i]
                rotor = rotorsDict[rotor]["cipher"]
                encryptedChar = encryptCharRotorIn(rotor, setting, position, encryptedChar)
                i -= 1

            encryptedChar = encryptCharReflector(reflectorDict, encryptedChar)

            i = 0

            for encryption in range(0, 3):
                setting = codeBookDict[day]["settings"]
                setting = setting[i]
                position = positions[i]
                rotor = codeBookDict[day]["rotors"]
                rotor = rotor[i]
                rotor = rotorsDict[rotor]["cipher"]
                encryptedChar = encryptCharRotorOut(rotor, setting, position, encryptedChar)
                i += 1

            i = 2
            encryptedText += encryptedChar
            j += 1
            if j % 5 == 0:
                encryptedText += ' '

        else:
            encryptedText += letter
            j += 1
            if j % 5 == 0:
                encryptedText += ' '

    print('Encrypted text: ', encryptedText)

    return encryptedText


if __name__ == '__main__':
    codeBookDict = {1: {"rotors": ["I", "II", "III"], "settings": "ABC", "positions": "DEF"},
                    2: {"rotors": ["II", "III", "IV"], "settings": "JBK", "positions": "TUV"},
                    3: {"rotors": ["III", "I", "IV"], "settings": "OFK", "positions": "UFJ"},
                    4: {"rotors": ["IV", "V", "IV"], "settings": "EUC", "positions": "LCN"},
                    5: {"rotors": ["V", "IV", "I"], "settings": "KWE", "positions": "IRN"},
                    6: {"rotors": ["II", "IV", "V"], "settings": "QIY", "positions": "DUB"},
                    7: {"rotors": ["III", "I", "IV"], "settings": "XOT", "positions": "QMV"},
                    8: {"rotors": ["II", "I", "IV"], "settings": "PLN", "positions": "PZM"},
                    9: {"rotors": ["II", "III", "I"], "settings": "QAZ", "positions": "KUR"},
                    10: {"rotors": ["IV", "I", "V"], "settings": "CVB", "positions": "LRU"},
                    11: {"rotors": ["V", "III", "I"], "settings": "NHY", "positions": "API"},
                    12: {"rotors": ["II", "IV", "I"], "settings": "UIF", "positions": "CPU"},
                    13: {"rotors": ["I", "II", "V"], "settings": "GRT", "positions": "NPC"},
                    14: {"rotors": ["I", "III", "II"], "settings": "TIV", "positions": "PCB"},
                    15: {"rotors": ["II", "I", "III"], "settings": "ZNM", "positions": "NTV"},
                    16: {"rotors": ["III", "IV", "V"], "settings": "TUI", "positions": "KFC"},
                    17: {"rotors": ["III", "II", "I"], "settings": "EDM", "positions": "GTA"},
                    18: {"rotors": ["I", "V", "IV"], "settings": "BLF", "positions": "RGB"},
                    19: {"rotors": ["II", "III", "IV"], "settings": "ELF", "positions": "UFC"},
                    20: {"rotors": ["III", "IV", "I"], "settings": "BAM", "positions": "JKL"},
                    21: {"rotors": ["IV", "III", "V"], "settings": "GUN", "positions": "LRP"},
                    22: {"rotors": ["II", "III", "IV"], "settings": "SON", "positions": "TQO"},
                    23: {"rotors": ["I", "III", "IV"], "settings": "RUM", "positions": "RPG"},
                    24: {"rotors": ["IV", "I", "II"], "settings": "LIV", "positions": "LMG"},
                    25: {"rotors": ["III", "V", "II"], "settings": "SUM", "positions": "FLY"},
                    26: {"rotors": ["II", "III", "I"], "settings": "JFK", "positions": "RED"},
                    27: {"rotors": ["IV", "II", "I"], "settings": "UPS", "positions": "NEW"},
                    28: {"rotors": ["II", "III", "V"], "settings": "TTS", "positions": "OLD"},
                    29: {"rotors": ["V", "IV", "II"], "settings": "AFK", "positions": "NOP"},
                    30: {"rotors": ["II", "I", "IV"], "settings": "RKO", "positions": "SPY"}}

    rotorsFile = open("rings.json", "r")
    jsonRotors = rotorsFile.read()
    rotorsDict = json.loads(jsonRotors)

    reflectorFile = open("reflector.json", "r")
    jsonReflector = reflectorFile.read()
    reflectorDict = json.loads(jsonReflector)

    while 1:
        print('Type day number between 1 and 30 to choose from these days:\n', codeBookDict)
        day = int(input())
        if 1 <= day <= 30:
            break
        else:
            print('You typed wrong number try again')

    text = input('Type text to be encrypted\n')

    encryptedText = encryptText(codeBookDict, rotorsDict, reflectorDict, day, text)

    encryptedTextFile = open("encrypted text.txt", "w")
    encryptedTextFile.write(encryptedText)

    rotorsFile.close()
    reflectorFile.close()
    encryptedTextFile.close()









