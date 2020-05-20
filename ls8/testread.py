import os
print(os.path.abspath("ls8/print8.ls8"))

with open(os.path.abspath("ls8/print8.ls8"), 'r') as print8:
    for p in print8:
        printMe = ''
        for c in p:
            if c != str(1) and c != str(0):
                break
            else:
                printMe = printMe + c
        if len(printMe) > 0:
            print(printMe)