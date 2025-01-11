from nltk.corpus import words

# nltk.download('words')

englishvocab = set(words.words())
gamestartinput = ""

totcounter = 1
suboink = 0
addoink = 0
froink = 0
boink = 0

gamegoing = False
checkword = False
wordinlist = False
goink = False
goinktype = ""

prevword= ""
word = ""
endingword = ""
totlist = []

def halflength(word):       #half life gap
    return int(-(-len(word) // 2))

def checkboink(word1, word2):
    i=0
    while(word1[i]==word2[i]):
        i+=1
    if i>=halflength(word1):
        return True
    else:
        return False

def checkfroink(word1, word2):
    i=1
    while(word1[-i]==word2[-i]):
        i+=1
    if i-1>=halflength(word1):
        return True
    else:
        return False

print("TRAIN OF THOUGHT")
print("==================")
print("Type 'tot start' to start")
print("Type 'tot info' to see game info")
print("Input 'tot end' during a game to end it\n")


while not gamegoing:
    gamestartinput = input()
    if gamestartinput == "tot start":
        gamegoing = True
    if gamestartinput == "tot info":
        print("\nTRAIN OF THOUGHT PREMISE")
        print("=================================")
        print("Pick a starting word and ending word")
        print("You then manipulate the starting word into other words until you reach the ending word")
        print("This word manipulation is known as a GOINK (GOOD + LINK)")
        print("Most plurals of words (ending with s) may not be counted as a GOINK")
        print("If you want a challenge, then try to get to the ending word with the least GOINKs")

        print("\nGOINK TYPES")
        print("================")
        print("SUBOINK (SUBTRACTION + GOINK): Removing parts from the previous word")
        print("Eg: cardiovascular → cardio || lobbyer → bye")
        print("\nADDOINK (ADDITION + GOINK): Adding parts to the previous word")
        print("Eg: fat → fatty || pock → pickpocket")
        print("\nFROINK (FRONT + GOINK): Changing at least the front half of the previous word")
        print("Eg: preserved → deserved || syndetic → eidetic")
        print("\nBOINK (BACK + GOINK): Changing at least the back half of the previous word")
        print("Eg: round → rouse || production → productive")
        print("\nFor FROINKS and BOINKS: The GOINKed word needs to retain at least 50% (rounded up) of the previous word")
        print("Eg: 5 letter word * 0.5 = 2.5 = 3(rounded up) letters on the other half that should be kept the same")
        print("MELANcholy → MELANin = VALID BOINK (5 letters retained)")
        print("seatbELT → smELT = INVALID FROINK (only 3 letters retained)")


if gamegoing:
    print("\nTRAIN OF THOUGHT GAME")
    print("============================")
    while not checkword:
        prevword = input("Input the starting word: ")
        checkword = prevword in englishvocab
        if not checkword:
            print("Not a real single word!")
    totlist.append(prevword)
    checkword = False
    while not checkword:
        endingword = input("Input the ending word: ")
        checkword = endingword in englishvocab
        if not checkword:
            print("Not a real single word!")
        elif endingword == prevword:
            print("Cannot make the ending word the starting word!")
            checkword=False
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
        
        # if word == "tot end":
        #     gamegoing = False
        #     break

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
            else:
                if checkfroink(prevword,word):
                    goink = True
                    goinktype = "FROINK!\n"
                    froink +=1
                elif checkboink(prevword,word):
                    goink = True
                    goinktype = "BOINK!\n"
                    boink +=1

        if not goink:
            if wordinlist:
                print("Word already used!\n")
                wordinlist=False
            else:
                print("Not a valid goink!\n")
            checkword = False
        else:
            print(goinktype)
            if word == endingword:
                gamegoing = False
                totlist.append(endingword)
                break
       
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
print("FROINKS:",froink)
print("BOINKS:",boink)
print("\nRun the program again to play again")
