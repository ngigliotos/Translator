#Contains a the classes and functions for words and particles for english and
#japanese


#A class for all the words in the dictionary that contains the word in both
#enlgish and japanese, and has the romanji of each word along with it's
#type and if it is a verb it's conjugations. When words are entered into the
#dictionary they must have all of these after the word (up till the NONE)
class Word:
    def __init__(self, romanji, hiragana, meaning, wordType, verbConjugation = None, uniqueRomanji = None, verbType = None):
        self.romanji = romanji
        self.hiragana = hiragana
        self.meaning = meaning
        self.type = wordType
        self.verbConjugation = verbConjugation
        self.uniqueRomanji = uniqueRomanji
        self.verbType  = verbType

    def __str__(self):
        return self.hiragana

    def PrintHiragana(self):
        print(self.hiragana)

    def PrintRomanji(self):
        print(self.romanji)

    def PrintMeaning(self):
        print(self.meaning)

    #Conjugate japanese verbs depending on the tense
    def Conjugate(self):
        if (self.verbConjugation == None):
            return
        else:
            if (self.verbConjugation == 'u'):
                newRomanji = self.romanji
                newRomanji = list(newRomanji)
                newRomanji[len(newRomanji) - 1] = 'i'
                newRomanji = ''.join(newRomanji)
                newRomanji += 'masu'
                return newRomanji
            elif (self.verbConjugation == 'ru'):
                newRomanji = self.romanji
                newRomanji = list(newRomanji)
                newRomanji.pop()
                newRomanji.pop()
                newRomanji = ''.join(newRomanji)
                newRomanji += 'masu'
                return newRomanji
            elif (self.verbConjugation == 'unique'):
                if (self.romanji == 'desu'):
                    return self.romanji
                else:
                    return self.uniqueRomanji + 'masu'
            else:
                return

#A class for all the particles in japanese and english, it has the same
#requirements as the words
class Particle:
    def __init__(self, romanji, hiragana, meanings, requirements):
        self.romanji = romanji
        self.hiragana = hiragana
        self.meanings = meanings
        self.requirements = requirements
        self.type = 'particle'


    def __str__(self):
        return self.hiragana

#This function turns all of the words from the word list into a word class
#variable and puts them into a list
def MakeWords():
    wordsFile = open("Words.txt", encoding="utf8")
    newWord = wordsFile.readline()
    newWordList = newWord.split()
    words = []
    while newWord.strip() != 'PARTICLES':
        for i in range(len(newWordList[2])):
            if (newWordList[2][i] == ';'):
                tempList = []
                tempList[:0] = newWordList[2]
                tempList[i] = ' '
                newString = ''.join(tempList)
                newWordList[2] = newString
                break

        if (len(newWordList) == 7 and newWordList[3] == 'verb'):
            words.append(Word(newWordList[0], newWordList[1], newWordList[2], newWordList[3], newWordList[4], newWordList[5], newWordList[6]))
        elif (len(newWordList) == 6 and newWordList[3] == 'verb'):
            words.append(Word(newWordList[0], newWordList[1], newWordList[2], newWordList[3], newWordList[4], newWordList[5]))
        else:
            words.append(Word(newWordList[0], newWordList[1], newWordList[2], newWordList[3]))
        newWord = wordsFile.readline()
        newWordList = newWord.split()

    wordsFile.close()
    return words

#This does the same as word list but with particles
def MakeParticles():
    wordsFile = open("Words.txt", encoding="utf8")
    newWord = wordsFile.readline()
    newWordList = newWord.split()
    particles = []

    while newWord.strip() != "PARTICLES":
        newWord = wordsFile.readline()

    newWord = wordsFile.readline()
    newWordList = newWord.split(';')
    while newWord:
        particleMeanings = newWordList[0].split()
        particleRequirements = newWordList[1].split()
        if (len(particleMeanings) > 3):
            tempList = []

            for i in range(2, len(particleMeanings)):
                tempList.append(particleMeanings[i])

            particleMeanings[2] = tempList
        else:
            tempList = []
            tempList.append(particleMeanings[2])
            particleMeanings[2] = tempList


        particles.append(Particle(particleMeanings[0], particleMeanings[1], particleMeanings[2], particleRequirements))

        newWord = wordsFile.readline()
        newWordList = newWord.split(';')

    wordsFile.close()
    return particles
