import time
import sys
def displayBanner():
    banner = open('../banner/banner.txt', 'r', encoding = "utf-8")
    print(banner.read() + " ", end = '')

    while True:
        choice = input()
        if choice == 'y':
            break
        elif choice == 'n':
            sys.exit()
        else:
            print("Not valid, retry: ", end = '')
