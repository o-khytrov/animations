if __name__ == "__main__":
    number = 325
    tmp = number
    bin = ""
    while tmp > 0:
        print(tmp)
        bin += "1" if tmp % 2 else "0"
        tmp = int(tmp / 2)
    print(bin)
