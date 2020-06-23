#Translates english to japanese


import Characters
import Translate

words = Characters.MakeWords()
particles = Characters.MakeParticles()



#Big function that converts japanese to english
def ToJapanese(sentence):
    wordList = sentence.split()
    sentenceList = []
    newSentenceHiragana = ''
    newSentenceRomanji = ''
    sentenceList = FindTranslation(wordList)

    question = False
    for i in sentenceList:
        if i.type == 'question':
            question = True

    if (question):
        newSentenceList = FormatQuestionSentence(sentenceList)

    else:
        newSentenceList = FormatSentence(sentenceList)

    return BuildSentence(newSentenceList, question)



#Gets the word variable and translation for each word the user entered
def FindTranslation(wordList):
    sentenceList = []
    for i in wordList:
        if (i != 'the'):
            sentenceList.append(i)

    #Translate words that arent names or particles as well as remove or add words
    #when needed as the languages are very different
    removeIndexes = []
    checkNext = True
    for i in range(len(sentenceList)):
        if (checkNext):
            for j in words:
                    #Check for translations that have two words
                if (i < len(sentenceList) - 1):
                    twoWords = sentenceList[i] + ' ' + sentenceList[i + 1]
                else:
                    twoWords = ''
                if (twoWords == j.meaning):
                    sentenceList[i] = j
                    removeIndexes.append(i + 1)
                    checkNext = False
                    break;
                elif (sentenceList[i] == j.meaning or sentenceList[i] == j.meaning + 's'):
                    sentenceList[i] = j
                    break;
                elif (sentenceList[i] == 'is' and j.meaning == 'am'):
                    sentenceList[i] = j
                    break;
        else:
            checkNext = True

    RemoveAtIndexes(sentenceList, removeIndexes)

    #Check if it is a particle
    for i in range(len(sentenceList)):
        if (not (isinstance(sentenceList[i], Characters.Word))):
            for j in particles:
                if (sentenceList[i] in j.meanings and i < len(sentenceList) - 1):
                    wordType = sentenceList[i + 1].type
                    for k in range(len(j.meanings)):
                        if (sentenceList[i] == j.meanings[k] and j.requirements[k] == wordType):
                            sentenceList[i] = j


        #Otherwise its a name
    for i in range(len(sentenceList)):
        if (not (isinstance(sentenceList[i], Characters.Word)) and not (isinstance(sentenceList[i], Characters.Particle))):
            sentenceList[i] = Characters.Word(sentenceList[i], Translate.TranslateHiragana(sentenceList[i]), sentenceList[i], 'name')

    return sentenceList



#Puts the words in the proper order for a normal japanese sentence
def FormatSentence(sentenceList):
    newSentenceList = []

    for i in range(7):
        for j in range(len(sentenceList)):
            if (isinstance(sentenceList[j], str) or sentenceList[j].type == 'particle'):
                pass
            #Looking for pronoun
            elif ((sentenceList[j].type == 'pronoun' or sentenceList[j].type == 'name') and i == 0):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for time
            elif (sentenceList[j].type == 'time' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 2):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 3):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            elif ((sentenceList[j].type == 'adverb' or sentenceList[j].type == 'adverbN') and i == 4):
                newSentenceList.append(sentenceList[j])

            #Looking for adjective
            elif (sentenceList[j].type == 'adjective' and i == 5):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 6):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

    return newSentenceList



#Puts the words in the proper order for a question japanese sentence
def FormatQuestionSentence(sentenceList):
    newSentenceList = []

    for i in range(5):
        for j in range(len(sentenceList)):
            if (isinstance(sentenceList[j], str) or sentenceList[j].type == 'particle'):
                pass
            #Looking for pronoun
            elif (sentenceList[j].type == 'pointer' and i == 0):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for pronoun
            elif (sentenceList[j].type == 'pronoun' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for place
            elif (sentenceList[j].type == 'place' and i == 1):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for noun
            elif (sentenceList[j].type == 'noun' and i == 2):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

            #Looking for adjective
            elif (sentenceList[j].type == 'question' and i == 3):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j + 1])
                newSentenceList.append(sentenceList[j])

            #Looking for verb
            elif (sentenceList[j].type == 'verb' and i == 4):
                if (CheckParticle(sentenceList, j)):
                    newSentenceList.append(sentenceList[j])
                    newSentenceList.append(sentenceList[j - 1])
                else:
                    newSentenceList.append(sentenceList[j])

    return newSentenceList



#Builds a translated sentence out of the list it was given
def BuildSentence(newSentenceList, question):
    newSentenceHiragana = ''
    newSentenceRomanji = ''

    for i in range(len(newSentenceList)):
        if (newSentenceList[i].type == 'verb'):
            if (i > 0):
                if(newSentenceList[i - 1].type == 'adverbN'):
                    negativeFormList = list(newSentenceList[i].Conjugate())
                    negativeFormList.pop()
                    negativeForm = ''.join(negativeFormList)
                    negativeForm += 'en'
                    newSentenceHiragana += Translate.TranslateHiragana(negativeForm)
                    newSentenceRomanji += negativeForm
                else:
                    newSentenceHiragana += Translate.TranslateHiragana(newSentenceList[i].Conjugate())
                    newSentenceRomanji += newSentenceList[i].Conjugate()
            else:
                newSentenceHiragana += Translate.TranslateHiragana(newSentenceList[i].Conjugate())
                newSentenceRomanji += newSentenceList[i].Conjugate()

        elif (newSentenceList[i].type == 'name'):
            newSentenceHiragana += newSentenceList[i].hiragana + 'さん'
            newSentenceRomanji += newSentenceList[i].romanji + 'san'
        else:
            newSentenceHiragana += newSentenceList[i].hiragana
            newSentenceRomanji += newSentenceList[i].romanji
        newSentenceHiragana += ' '
        newSentenceRomanji += ' '


        if (newSentenceList[i].type == 'noun'):
            newSentenceHiragana += 'を'
            newSentenceHiragana += ' '
            newSentenceRomanji += 'wo'
            newSentenceRomanji += ' '

        elif (newSentenceList[i].type == 'pronoun' or newSentenceList[i].type == 'name' or newSentenceList[i].type == 'pointer'):
            newSentenceHiragana += 'は'
            newSentenceHiragana += ' '
            newSentenceRomanji += 'ha'
            newSentenceRomanji += ' '

    if(question):
        newSentenceHiragana += 'か'
        newSentenceRomanji += 'ka'

    return [newSentenceHiragana, newSentenceRomanji]



#Checks whether or not the word is a particle
def CheckParticle(sentenceList, index):
    if (index >= 1):
        if sentenceList[index - 1].type == 'particle':
            return True

    else:
        return False


#Removes words from the given list where specified
def RemoveAtIndexes(sentenceList, indexes):
    for i in indexes:
        sentenceList.pop(i)
