#!/bin/env python3
#start of sorter
def bubbleSort(unsorted):
    noSwaps = True
    while noSwaps == True:
        noSwaps = False
        for item in range(len(unsorted)-1):
            if unsorted[item] > unsorted[item+1]:
                temp = unsorted[item+1]
                unsorted[item+1] = unsorted[item]
                unsorted[item] = temp
                noSwaps = True
        
def Sort():
    with open("Sort.txt", mode="r", encoding="utf-8") as myFile:
        Things = myFile.read().splitlines()
        tmp1 = myFile.read().splitlines()
    bubbleSort(Things)

    with open("Sort.txt",mode="w",encoding="utf-8") as myFile:
        for Thing in Things:
            myFile.write(Thing+"\n")

def reload():
    print ("")
    TXTsorter()
    
def TXTsorter():
    with open("Sort.txt",mode="w",encoding="utf-8") as myFile:
        print ("Welcome to the .txt Bubble Sorter v1.0!")
    print ("Please find a file called 'Sort.txt' and paste")
    print ("what you want to sort into it. After you do that,")
    print ("Save and close the document.")
    wait = str("n")
    while not wait == "ready":
        wait = input("Please type 'ready' to continue.. ")
    #fileNameImport = str(input("What is the .txt file named? Please enter the whole name, like 'cats.txt' "))
    print ("The file 'Sort.txt' will be sorted soon...")
    Sort()
    print ("Done!")
    print ("")
    if input("Would you like to quit? y/n ") == "n":
        reload()
        
TXTsorter()
print ("Thank you for useing the TXT sorter v1.6!")
quit()
