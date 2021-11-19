crypt = {
    "A": "T",
    "B": "I",
    "C": "M",
    "D": "E",
    "E": "O",
    "F": "D",
    "G": "A",
    "H": "N",
    "I": "S",
    "J": "F",
    "K": "R",
    "L": "B",
    "M": "C",
    "N": "G",
    "O": "H",
    "P": "J",
    "Q": "K",
    "R": "L",
    "S": "P",
    "T": "Q",
    "U": "U",
    "V": "V",
    "W": "W",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "0": "9",
    "1": "8",
    "2": "7",
    "3": "6",
    "4": "5",
    "5": "4",
    "6": "3",
    "7": "2",
    "8": "1",
    "9": "0"
}


def encrypt_password(password):
    password = password.upper()
    encrpyted_password = ""
    for ch in password:
        encrpyted_password += crypt[ch]
    return encrpyted_password


# in case in future if we implement forgot password functionality
def decrypt_password(encrypted_password):
    password = ""
    for ch in encrypted_password:
        password += [k for k, v in crypt.items() if v == ch][0]

    return password
