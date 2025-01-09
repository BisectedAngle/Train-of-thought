import nltk
from nltk.corpus import words

englishvocab = set(words.words())
gamestartinput = ""
gamegoing = False
checkword = False
totcounter = 1
word = ""
totlist = []

print("TRAIN OF THOUGHT")
print("==================")
print("Type 'tot start' to start")
print("Type 'tot rules' to see rules")
print("Input 'tot end' to end the game\n")

while not gamegoing:
    gamestartinput = input()
    if gamestartinput == "tot start":
        gamegoing = True
    if gamestartinput == "tot rules":
        print("Rules here\n")

while gamegoing:
    while not checkword:
        word = input("({}) input word: ".format(totcounter))
        if word == "tot end":
            gamegoing = False
            break
        else:
            checkword = word in englishvocab
            if not checkword:
                print("not a real single word!")
    checkword = False
    totcounter +=1
    