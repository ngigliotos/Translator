#Translates japanese to english


import Characters
import Translate

words = Characters.MakeWords()
particles = Characters.MakeParticles()


#Big function that uses the others to properly convert the sentence to english.
def ToEnglish(sentence):
    wordList = sentence.split()
    sentenceList = []

    for i in wordList:
        sentenceList.append(FindTranslation(i))

    #If the romanji ends witha  verb that ends with the letter n its a negative
    if(sentence[len(sentence) - 1] == 'n' and sentenceList[len(sentenceList) - 1].type == 'verb'):
        negative = True
    else:
        negative = False

    question = False
    for i in sentenceList:
        if (i.type == 'question'):
            question = True
        #Check if particle ka, remove it if so
        elif(i.type == 'particle' and i.romanji == 'ka'):
            question = True

    if question:
        sentenceList =  FormatQuestionSentence(sentenceList)
        return QuestionSentence(sentenceList)

    #If its not a question check if its a pointer sentence
    elif(sentenceList[0].type == 'pointer'):
        sentenceList =  FormatPointerSentence(sentenceList)
        return PointerSentence(sentenceList)

    elif(sentenceList[0].type == 'noun'):
        sentenceList =  FormatAdjectiveSentence(sentenceList)
        return AdjectiveSentence(sentenceList)

    #Lastly check if its the format of "I am noun"
    elif(sentenceList[0].type == 'pronoun'):
        for i in sentenceList:
            if (i.type == 'verb' and i.meaning == 'am'):
                sentenceList =  FormatPointerSentence(sentenceList)
                return PointerSentence(sentenceList)

    #Otherwise its a normal sentence
    sentenceList =  FormatNormalSentence(sentenceList)
    return NormalSentence(sentenceList, negative)


#Gets the word variable and translation of each word entered by the user
def FindTranslation(word):
    if (len(word) > 4):
        #Check if the last three letters are san, if so its a name
        if (word[len(word) - 1] == 'n' and word[len(word) - 2] == 'a' and word[len(word) - 3] == 's'):
            newWord = list(word)
            newWord.pop()
            newWord.pop()
            newWord.pop()
            word = ''
            for i in newWord:
                word += i
            return Characters.Word(word, Translate.TranslateHiragana(word), word, 'name')

    #Iterate through the words and try to find a match for the word they entered
    #if found translate the word, otherwise say it was not found
    for i in words:
        if (word == i.romanji):
            return i
        elif(i.type == 'verb'):
            if (word == i.Conjugate()):
                return i
            else:
                negativeFormList = list(i.Conjugate())
                negativeFormList.pop()
                negativeForm = ''.join(negativeFormList)
                negativeForm += 'en'
                if(word == negativeForm):
                    return i

    for i in particles:
        if (word == i.romanji):
            return i

    else:
        return Characters.Word(word, Translate.TranslateHiragana(word), word, 'name')

    print("Word", word, 'was not found.')
    return "Unknown"


#Makes an normal english sentence out of the word list passed to the function
def NormalSentence(newSentenceList, negative):

    newSentence = ''

    noPronoun = True
    for i in newSentenceList:
        if (i.type == 'pronoun' or i.type == 'name'):
            noPronoun = False
    if noPronoun:
        newSentenceList = FixSentence(newSentenceList)

    #Change to sentence Loop
    #Bool for if am needs to be changed to is
    changeAm = False

    for i in range(len(newSentenceList)):
        if (i == 0 and newSentenceList[i].type == 'noun'):
            changeAm = True
        if (newSentenceList[i].type == 'particle'):
            if (newSentenceList[i].romanji == 'ha'):
                pass
            elif (len(newSentenceList[i].meanings) > 1):
                if ((i + 1) <= len(newSentenceList) - 1):
                    for j in range(len(newSentenceList[i].requirements)):
                        if (newSentenceList[i + 1].type == newSentenceList[i].requirements[j]):
                            newSentence += newSentenceList[i].meanings[j]
                            break

            else:
                newSentence += newSentenceList[i].meanings[0]
        else:
            if (newSentenceList[i].type == 'place'):
                newSentence += 'the '
                newSentence += newSentenceList[i].meaning
            elif (newSentenceList[i].type == 'verb'):
                if(changeAm):
                    newSentence += 'is'
                    changeAm = False
                elif(i > 0 and negative):
                    if(newSentenceList[i - 1].type == 'adverbN'):
                        newSentence += newSentenceList[i].meaning
                    else:
                        newSentence += "didn't "
                        newSentence += newSentenceList[i].meaning
                else:
                    newSentence += newSentenceList[i].meaning
                if(i > 0):
                    #Check if a name preceeds it
                    if (newSentenceList[i - 1].type == 'name'):
                        newSentence += 's'
                    #if an adverb preceeds it check if a name preceed the adverb
                    elif((newSentenceList[i - 1].type == 'adverb' or newSentenceList[i - 1].type == 'adverbN') and i > 1):
                        if (newSentenceList[i - 2].type == 'name'):
                            newSentence += 's'
            else:
                newSentence += newSentenceList[i].meaning

        newSentence += ' '

    return [newSentence, newSentenceList]


#Puts the words in the right order for an english sentence
#(in japanese word order is different)
def FormatNormalSentence(sentenceList):
    newSentenceList = []

    for i in range(7):
        for j in range(len(sentenceList)):
            if (sentenceList[j] == "Unknown" or sentenceList[j].type == 'particle'):
                pass
            #Looking for pronoun
            elif ((sentenceList[j].type == 'pronoun' or sentenceList[j].type == 'name') and i == 0):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for adverb
            elif ((sentenceList[j].type == 'adverb' or sentenceList[j].type == 'adverbN') and i == 1):
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 2):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 3):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for adjective
            elif (sentenceList[j].type == 'adjective' and i == 4):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 5):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for time
            elif (sentenceList[j].type == 'time' and i == 6):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

    return newSentenceList

#Does the same thing as normal sentence but with different rules
#as pointers work different
def PointerSentence(newSentenceList):

    newSentence = ''

    if newSentenceList[0].type == 'pointer':

        for i in newSentenceList:
            if (i.type != 'particle'):
                if(i.type == 'verb' and i.meaning == 'am'):
                    newSentence += 'is'
                elif(i.type == 'noun'):
                    newSentence += 'a '
                    newSentence += i.meaning
                elif(i.type == 'place'):
                    newSentence += 'the '
                    newSentence += i.meaning
                else:
                    newSentence += i.meaning

                newSentence += ' '
    else:
        for i in range(len(newSentenceList)):
            if (newSentenceList[i].type != 'particle'):
                if(newSentenceList[i].type == 'verb' and newSentenceList[i].meaning == 'am'):

                    #Make sure we are in range
                    if(i > 0):
                        if(newSentenceList[i - 1].meaning.lower() != 'i'):
                            newSentence += 'are'
                        else:
                            newSentence += newSentenceList[i].meaning
                    else:
                        newSentence += newSentenceList[i].meaning


                elif(newSentenceList[i].type == 'noun'):
                    newSentence += 'a '
                    newSentence += newSentenceList[i].meaning
                elif(newSentenceList[i].type == 'noun'):
                    newSentence += 'the '
                    newSentence += newSentenceList[i].meaning
                else:
                    newSentence += newSentenceList[i].meaning

                newSentence += ' '

    return [newSentence, newSentenceList]


#Puts the words in proper order for a english pointer sentence
def FormatPointerSentence(sentenceList):
    newSentenceList = []

    for i in range(5):
        for j in range(len(sentenceList)):
            if (sentenceList[j] == "Unknown" or sentenceList[j].type == 'particle'):
                pass
            #Looking for pointer
            elif ((sentenceList[j].type == 'pointer' or sentenceList[j].type == 'pronoun') and i == 0):
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for name
            elif (sentenceList[j].type == 'name' and i == 2):
                newSentenceList.append(sentenceList[j])

            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 3):
                newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 4):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])


    return newSentenceList

#Does the same thing as normal sentence but with different rules
#as questions work different
def QuestionSentence(newSentenceList):

    #Bool of whether a space should be added after adding a word
    addSpace = True

    #Bool of whether or the verb is "is"
    notIs = False
    for i in words:
        if (i.meaning == 'am'):
            notIs = True
            break;

    newSentence = ''

    for i in range(len(newSentenceList)):
        if (newSentenceList[i].type == 'particle'):
            if (newSentenceList[i].romanji == 'ha'):
                addSpace = False
            elif (len(newSentenceList[i].meanings) > 1):
                if ((i + 1) <= len(newSentenceList) - 1):
                    for j in range(len(newSentenceList[i].requirements)):
                        if (newSentenceList[i + 1].type == newSentenceList[i].requirements[j]):
                            newSentence += newSentenceList[i].meanings[j]
                            break

            else:
                newSentence += newSentenceList[i].meanings[0]
        else:
            if (newSentenceList[i].type == 'place'):
                newSentence += 'the '
                newSentence += newSentenceList[i].meaning
            elif (newSentenceList[i].type == 'verb' and newSentenceList[i].romanji == 'desu'):
                newSentence += 'is'
            elif (newSentenceList[i].type == 'pronoun' and notIs):
                newSentence += 'do '
                newSentence += newSentenceList[i].meaning
            else:
                newSentence += newSentenceList[i].meaning

        if(addSpace):
            newSentence += ' '
        else:
            addSpace = True

    return [newSentence, newSentenceList]


#Puts the words in proper order for a english question sentence
def FormatQuestionSentence(sentenceList):
    newSentenceList = []

    for i in range(7):
        for j in range(len(sentenceList)):
            if (sentenceList[j] == "Unknown" or sentenceList[j].type == 'particle'):
                pass
            #Looking for question word
            elif (sentenceList[j].type == 'question' and i == 0):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for pronoun
            elif (sentenceList[j].type == 'pronoun' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 2):
                newSentenceList.append(sentenceList[j])

            #Looking for pointer
            elif (sentenceList[j].type == 'pointer' and i == 3):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 4):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 5):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for time
            elif (sentenceList[j].type == 'time' and i == 6):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

    return newSentenceList


#Puts the words in proper order for a english adjective sentence
def FormatAdjectiveSentence(sentenceList):
    newSentenceList = []

    for i in range(7):
        for j in range(len(sentenceList)):
            if (sentenceList[j] == "Unknown" or sentenceList[j].type == 'particle'):
                pass
            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 0):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for adjective
            elif (sentenceList[j].type == 'adjective' and i == 2):
                newSentenceList.append(sentenceList[j])


    return newSentenceList


#Does the same thing as normal sentence but with different rules
#as adjectives work different
def AdjectiveSentence(newSentenceList):
    notIs = False
    for i in words:
        if (i.meaning == 'am'):
            notIs = True
            break;

    newSentence = ''

    for i in range(len(newSentenceList)):
        if (newSentenceList[i].type == 'particle'):
            if (newSentenceList[i].romanji == 'ha'):
                addSpace = False
            elif (len(newSentenceList[i].meanings) > 1):
                if ((i + 1) <= len(newSentenceList) - 1):
                    for j in range(len(newSentenceList[i].requirements)):
                        if (newSentenceList[i + 1].type == newSentenceList[i].requirements[j]):
                            newSentence += newSentenceList[i].meanings[j]
                            break

            else:
                newSentence += newSentenceList[i].meanings[0]
        else:
            if (newSentenceList[i].type == 'place' or newSentenceList[i].type == 'noun'):
                newSentence += 'the '
                newSentence += newSentenceList[i].meaning
            elif (newSentenceList[i].type == 'verb' and newSentenceList[i].romanji == 'desu'):
                newSentence += 'is'
            elif (newSentenceList[i].type == 'pronoun' and notIs):
                newSentence += 'do '
                newSentence += newSentenceList[i].meaning
            else:
                newSentence += newSentenceList[i].meaning

        if(addSpace):
            newSentence += ' '
        else:
            addSpace = True

    return [newSentence, newSentenceList]


#Checks whether or not the current word is a particle
def CheckParticle(sentenceList, index):
    if ((index + 1) < len(sentenceList) - 1):
        if sentenceList[index + 1].type == 'particle':
            return True

    else:
        return False


#Used to reformat a normal sentence if there is no pronoun
def FixSentence(sentenceList):
    newSentenceList = []

    for i in range(6):
        for j in range(len(sentenceList)):
            if (sentenceList[j] == "Unknown" or sentenceList[j].type == 'particle'):
                pass
            #Looking for pronoun
            elif ((sentenceList[j].type == 'noun' or sentenceList[j].type == 'name') and i == 0):
                if (CheckParticle(sentenceList, j - 2)):
                    newSentenceList.append(sentenceList[j - 1])
                newSentenceList.append(sentenceList[j])

            #Looking for adverb
            elif ((sentenceList[j].type == 'adverb' or sentenceList[j].type == 'adverbN') and i == 1):
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 2):
                newSentenceList.append(sentenceList[j])

            #Looking for adjective
            elif (sentenceList[j].type == 'adjective' and i == 4):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 5):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for time
            elif (sentenceList[j].type == 'time' and i == 6):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

    return newSentenceList
