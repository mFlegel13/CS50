import sys
from cs50 import get_string

print("plaintext: ", end="")

key = int(sys.argv[1])
if key < 0:
    print("Usage: Key must be a positive number")
    sys.exit(1)

while True:
    plaintxt = get_string()
    if plaintxt == 0:
        continue
    else:
        break

plain = [char for char in plaintxt]
ciphertxt = []

for char in plain:
    if char.isupper():
        ciphertxt.append(chr(((ord(char) - ord('A') + key) % 26) + ord('A')))
    elif char.islower():
        ciphertxt.append(chr(((ord(char) - ord('a') + key) % 26) + ord('a')))
    else:
        ciphertxt.append(char)

print("ciphertext: ", end="")
print("".join(ciphertxt))