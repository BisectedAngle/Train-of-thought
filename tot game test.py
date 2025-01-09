import nltk
from nltk.corpus import words

# nltk.download('words')

englishvocab = set(words.words())
gamestartinput = ""

totcounter = 1
pionkcalc = 0
suboink = 0
addoink = 0

gamegoing = False
checkword = False
wordinlist = False
goink = False
goinktype = ""

prevword= ""
word = ""

totlist = []

print("TRAIN OF THOUGHT")
print("==================")
print("Type 'tot start' to start")
print("Type 'tot info' to see game info")
print("Input 'tot end' to end the game\n")

while not gamegoing:
    gamestartinput = input()
    if gamestartinput == "tot start":
        gamegoing = True
    if gamestartinput == "tot info":
        print("\nTRAIN OF THOUGHT PREMISE")
        print("=================================")
        print("First, you pick a starting word")
        print("You then manipulate this word into other words until you're sick of it")
        print("This word manipulation is known as a GOINK (GOOD + LINK)")

        print("\nGOINK TYPES")
        print("================")
        print("SUBOINK (SUBTRACTION + GOINK): Removing chunks from the previous word")
        print("Eg: cardiovascular → cardio || lobbyer → bye")
        print("\nADDOINK (ADDITION + GOINK): Adding chunks to the previous word")
        print("Eg: fat → fatty || pock → pickpocket")




if gamegoing:
    while not checkword:
        prevword = input("Input the starting word: ")
        checkword = prevword in englishvocab
        if not checkword:
            print("Not a real single word!")
    totlist.append(prevword)
    checkword = False
    print()

while gamegoing:
    while not goink: 
        while not checkword:
            print("Previous word:",prevword)
            word = input("({}) Input next word: ".format(totcounter))
            if word == "tot end":
                break
            else:
                checkword = word in englishvocab
                if not checkword:
                    print("Not a real single word!\n")
        
        if word == "tot end":
            gamegoing = False
            break

        if word in totlist:
            wordinlist = True
        else:
            if word in prevword:
                goink = True
                goinktype = "SUBOINK!\n"
                suboink+=1
            elif prevword in word:
                goink = True
                goinktype = "ADDOINK!\n"
                addoink+=1

        if not goink:
            if wordinlist:
                print("Word already used!\n")
                wordinlist=False
            else:
                print("Not a goink!\n")
            checkword = False
        else:
            print(goinktype)
       
    checkword = False
    goink = False
    totcounter +=1
    totlist.append(word)
    prevword = word
    word = ""

print("\nTRAIN OF THOUGHT GAME STATS")
print("================================")
totlist.pop(len(totlist)-1)
print("You totted {} words in total:".format(len(totlist)))
print(totlist[0],end='')
for i in range(1,len(totlist)):
    print(" →",totlist[i],end='')

print("\n\nADDOINKS:",addoink)
print("SUBOINKS:",suboink)
