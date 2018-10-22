from cs50 import get_int

def main():
    while True:
        print("Height: ", end = "")
        height = get_int()
        if height >= 0 and height <= 23:
            break

    for rows in range(height):
        for space in range(height - rows - 1):
            print(" ", end = "")
        for hashes in range(height - rows, height + 1):
            print("#", end = "")
        print("  ", end = "")
        for hashes in range(height - rows, height + 1):
            print("#", end = "")
        print()

if __name__ == "__main__":
    main()

