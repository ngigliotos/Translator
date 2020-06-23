#The main function, this file handles the menu and calls the functions
#in other files when needed to translate

import Translate
import Characters
import English
import Japanese
import Checker
import Error

def main():
    words = English.words
    particles = English.particles
    using = True
    corrections = True
    print("Welcome to a terrible low level japanese translator!")
    while (using):
        try:
            if (corrections):
                print("Corrections are on")
            else:
                print("Corrections are off")
            print("Press 1 to translate japanese to english")
            print("Press 2 to translate english to japanese")
            print("Press 3 to toggle corrections on or off")
            print("Press 4 to quit")
            choice = int(input())
            while (choice > 4 or choice < 1 ):
                print("Please select a valid choice")
                choice = int(input())

            if (choice == 1):
                print("Please enter a space between each word AND particle")
                print("Please enter the sentence you would like to translate")
                sentence = input()
                hiraganaSentence = Translate.TranslateHiragana(sentence)
                print()
                print('Hiragana: ', hiraganaSentence)
                sentenceList = English.ToEnglish(sentence)
                print('Translation: ', sentenceList[0])
                print()
                if (corrections):
                    Checker.IsCorrect(sentenceList[1], sentenceList[0])

            elif(choice == 2):
                print("Please enter the sentence you would like to translate")
                sentence = input()
                japaneseSentences = Japanese.ToJapanese(sentence)
                print()
                print('Romanji:',japaneseSentences[1])
                print('Hiragana:', japaneseSentences[0])
                print()

            elif(choice == 3):
                if(corrections):
                    print("Corrections have been switched to off")
                    corrections = False
                else:
                    print("Corrections have been switched to on")
                    corrections = True

            elif(choice == 4):
                print("Thanks for using it :)")
                using = False
        except Error.UnknownWordError as e:
            print(e)
        except:
            print("Please enter a valid entry")



main()
