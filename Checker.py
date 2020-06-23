#Checks whether or not the japanese grammar entered is correct. If checking is
#disabled this file has little use

import Characters
import Japanese

#Parent function that uses the most of the other functions to check whether or
#not the sentence is correct
def IsCorrect(sentenceList, sentence):
    #Check if the sentence is negative
    wordList = sentence.split()
    for i in wordList:
        if (i == "didn't"):
            negative = True
            break
        else:
            negative = False

    #Drop all particles in the sentence and only take the words
    noParticleSentence = []
    for i in sentenceList:
        if (isinstance(i, Characters.Word)):
            noParticleSentence.append(i)

    #Auto fill in all the particles based on what the word types are and what it starts with

    if(noParticleSentence[0].type == 'pointer'):
        correctSentence = FormatPointerSentence(sentenceList, noParticleSentence)

    elif(noParticleSentence[0].type == 'pronoun' or noParticleSentence[0].type == 'noun'):
        for i in sentenceList:
            if (i.type == 'verb' and i.meaning == 'am'):
                correctSentence =  FormatPointerSentence(sentenceList, noParticleSentence)
                break;
            else:
                correctSentence = FormatSentence(sentenceList, noParticleSentence, negative)
    else:
        correctSentence = FormatSentence(sentenceList, noParticleSentence, negative)

    #Compare the two, if there is any difference then tell the user and print their
    #sentence and the computers for them to look over
    if (correctSentence != sentence):
        indexDifferences = FindDifferences(correctSentence, sentence)
        japaneseSentences = Japanese.ToJapanese(correctSentence)
        print("There may have been a grammar mistake, did you mean:")
        print("Romanji: ", japaneseSentences[1])
        print("Hiragana: ", japaneseSentences[0])
        print("Translation: ", correctSentence)
        print()


def FormatSentence(sentenceList, noParticleSentence, negative):
    #Add the particles based on context and see if it matches the translation


    #Correct sentence starts with space to account for particle 'ha'
    correctSentence = ' '
    verbType = ''
    #Bool for if s must be added to verb
    AddEnding = False
    #Bool for if its a question
    isQuestion = False
    for i in sentenceList:
        if (i.type == 'question'):
            isQuestion = True
            #If its a quesion remove additional space
            correctSentence = ''

    #Go through the whole sentence and add words when needed
    for i in range(len(noParticleSentence)):
        #If the first word is a noun then there is no particle "ha"
        #so the space is removed
        if(i == 0 and noParticleSentence[i].type == 'noun'):
            correctSentence = ''
            changeAm = True
        #If the word is a name add honorific "san"
        if(noParticleSentence[i].type == 'name' and CheckIndex(i, noParticleSentence)):
            correctSentence += noParticleSentence[i].meaning
            AddEnding = True

        #If it is a noun add particles and translation
        elif (noParticleSentence[i].type == 'noun'):
            correctSentence += 'the '
            correctSentence += noParticleSentence[i].meaning
            if (CheckIndex(i, noParticleSentence)):
                if (noParticleSentence[i + 1].type == 'place'):
                    if (verbType == 'action'):
                        correctSentence += ' '
                        correctSentence += 'at'
                    elif (verbType == 'movement'):
                        correctSentence += ' '
                        correctSentence += 'to'
                elif(noParticleSentence[i + 1].type == 'time'):
                    correctSentence += ' '
                    correctSentence += 'on'

        #If it is a place check for time and if so add differnt particles
        elif(noParticleSentence[i].type == 'place'):
            correctSentence += 'the '
            correctSentence += noParticleSentence[i].meaning
            if(CheckIndex(i, noParticleSentence)):
                if(noParticleSentence[i + 1].type == 'time'):
                    correctSentence += ' '
                    correctSentence += 'on'

        #If it is a verb then conjuagte the verb prooeprly
        elif (noParticleSentence[i].type == 'verb'):
            if (isQuestion and noParticleSentence[i].meaning == 'am'):
                correctSentence += 'is'
            elif(i > 0 and negative):
                if(noParticleSentence[i - 1].type == 'adverbN'):
                    correctSentence += noParticleSentence[i].meaning
                else:
                    correctSentence += "didn't "
                    correctSentence += noParticleSentence[i].meaning
            else:
                correctSentence += noParticleSentence[i].meaning
            if(AddEnding):
                correctSentence += 's'
                AddEnding = False
            verbType = noParticleSentence[i].verbType
            if(CheckIndex(i, noParticleSentence)):
                if (noParticleSentence[i + 1].type == 'place'):
                    if (verbType == 'action'):
                        correctSentence += ' '
                        correctSentence += 'at'
                    elif (verbType == 'movement'):
                        correctSentence += ' '
                        correctSentence += 'to'
                elif(noParticleSentence[i + 1].type == 'time'):
                    correctSentence += ' '
                    correctSentence += 'on'

        elif(noParticleSentence[i].type == 'pronoun' and isQuestion):
            correctSentence += 'do '
            correctSentence += noParticleSentence[i].meaning

        else:
            correctSentence += noParticleSentence[i].meaning

        correctSentence += ' '

    return correctSentence


def FormatPointerSentence(sentenceList, noParticleSentence):

    #Works the same as format sentence but pointers change the
    #rules a bit so this accounts for the rules
    newSentence = ''

    for i in noParticleSentence:
        if i.type == 'adjective':
            adjective = True
            break
        else:
            adjective = False

    if (noParticleSentence[0].type == 'pointer' or noParticleSentence[0].type == 'noun'):

        for i in noParticleSentence:
            if(i.type == 'verb' and i.meaning == 'am'):
                newSentence += 'is'
            elif(i.type == 'noun'):
                if adjective:
                    newSentence += 'the '
                else:
                    newSentence += 'a '
                newSentence += i.meaning
            elif(i.type == 'place'):
                newSentence += 'the '
                newSentence += i.meaning
            else:
                newSentence += i.meaning

            newSentence += ' '

    else:
        for i in range(len(noParticleSentence)):
            if(noParticleSentence[i].type == 'verb' and noParticleSentence[i].meaning == 'am'):

                #Make sure we are in range
                if(i > 0):
                    if(noParticleSentence[i - 1].meaning.lower() != 'i'):
                        newSentence += 'are'

                    else:
                        newSentence += noParticleSentence[i].meaning
                else:
                    newSentence += noParticleSentence[i].meaning

            elif(noParticleSentence[i].type == 'noun'):
                newSentence += 'a '
                newSentence += noParticleSentence[i].meaning
            elif(noParticleSentence[i].type == 'noun'):
                newSentence += 'the '
                newSentence += noParticleSentence[i].meaning
            else:
                newSentence += noParticleSentence[i].meaning

            newSentence += ' '

    return newSentence

#Check if there are any differences between the sentences
def FindDifferences(correctSentence, sentence):
    correctSentenceList = correctSentence.split()
    sentenceList = sentence.split()
    indexDifferences = []
    if (len(correctSentenceList) == len(sentenceList)):
        for i in range (len(correctSentenceList)):
            if correctSentenceList[i] != sentenceList[i]:
                indexDifferences.append(i)

    elif (len(correctSentenceList) > len(sentenceList)):
        for i in range (len(sentenceList)):
            if correctSentenceList[i] != sentenceList[i]:
                indexDifferences.append(i)

    elif (len(correctSentenceList) < len(sentenceList)):
        for i in range (len(correctSentenceList)):
            if correctSentenceList[i] != sentenceList[i]:
                indexDifferences.append(i)

    return indexDifferences

#Makes sure the index is not out of range
def CheckIndex(index, myList):
    return index < (len(myList) - 1)
