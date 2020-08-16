import speech_recognition as sr
from random import sample
import jellyfish
import os

# Global Variables.
recognizer = sr.Recognizer()

# Paths archives.
PATH_REPORT = 'Files\Report.txt'
PATH_BEGINNER = 'Files\Phrases\Beginner.txt'
PATH_INTERMEDIATE = 'Files\Phrases\Intermediate.txt'
PATH_ADVANCED = 'Files\Phrases\Advanced.txt'
PATH_CATCH_PHRASES = 'Files\Phrases\Catch Phrase.txt'
PATH_MOVIES_SERIES = 'Files\Phrases\Movies and series.txt'

# Time microphone.
TIME_BEGINNER = 5
TIME_INTERMEDIATE = 7
TIME_ADVANCED = 10
TIME_CATCH_PHRASES = 7
TIME_MOVIES_SERIES = 5
TIME_FREE = 5

# Clear screen.
if os.name == 'nt':
    CLEAR = 'cls'
else:
    CLEAR = 'clear'


# Return 0 for free mode.
# Return 1 for Phrases Beginner.
# Return 2 for Phrases Intermediate.
# Return 3 for Phrases Advanced.
# Return 4 for Catch Phrases.
# Return 5 for Movies and Series.
def menu():
    choice = 0

    while choice < 1 or choice > 2:
        choice = int(input("What do you want to do?\n"
                           "1 - Train phrases\n"
                           "2 - Free mode\n"))
        os.system(CLEAR)
    if choice == 1:
        choice = 0
        while choice < 1 or choice > 5:
            choice = int(input("1 - Beginner\n"
                               "2 - Intermediate\n"
                               "3 - Advanced\n"
                               "4 - Catch Phrases\n"
                               "5 - Movies and Series\n"))
            os.system(CLEAR)
        return choice
    else:
        return 0


# Get phrases randomly from files.
# Receive quantity of phrases and the path of file.
# Returns a list of English phrases and a translation list.
def get_phrases(path):
    list_phrases = []
    list_translate = []
    cont = 0
    quantity = 0

    with open(path, 'r', encoding='utf8') as phrases:
        # Calculates number of files in the file.
        file_lines = sum(1 for _ in phrases)
        if file_lines == 0:
            print("This section has no phrases.")
            os.system(exit())
        # Back to the beginning of the file.
        phrases.seek(0)
        if phrases is None:
            print("File not found.")
            os.system(exit())
        while quantity < 1 or quantity > file_lines:
            print("This section has ", file_lines, " sentences.")
            quantity = int(input("How many phrases do you want to train: "))
        # Get phrases randomly.
        numbers = sample(range(0, file_lines), quantity)
        for line in phrases:
            if cont in numbers:
                # Remove \n
                line = line.rstrip()
                en, pt = line.split(';')
                list_phrases.append(en)
                list_translate.append(pt)
            cont += 1
    return list_phrases, list_translate


# Get the audio from the microphone.
# Receive microphone activation time.
# Returns the text the user spoke or None if it was not possible to capture.
def get_audio(time):
    try:
        with sr.Microphone() as source:
            if source is None:
                print("Microphone not found.")
                os.system(exit())
            recognizer.adjust_for_ambient_noise(source)
            print("Talk!")
            audio_data = recognizer.record(source, duration=time)
            text = recognizer.recognize_google(audio_data)
            if text == 'stop':
                return 0
            return text
    except:
        print("Was't possible convert you speech to text!\n")


# Hit Rate using Levenshtein distance algorithm.
# Receive phrases and the answers.
def accuracy(phrases, translate, answers):
    final_score = []
    punctuation = ['"', '?', '!', '.', ':', '+', '-', "'", '/', '’']
    # Phrase treatment.
    # Remove punctuation and uppercase.
    for x in range(0, len(phrases)):
        phrases[x] = phrases[x].lower()
        answers[x] = answers[x].lower()
        for char in punctuation:
            if char in phrases[x]:
                phrases[x] = phrases[x].replace(char, '')
            if char in answers[x]:
                answers[x] = answers[x].replace(char, '')
        # Corrects negative score error.
        if len(phrases[x]) > len(answers[x]):
            divisor = len(phrases[x])
        else:
            divisor = len(answers[x])
        # Show the phrase, translation and score.
        score = 100 - (jellyfish.levenshtein_distance(phrases[x], answers[x]) * 100 / divisor)
        final_score.append(score)
    report(phrases, translate, answers, final_score)


# Report results and saves user history.
# Receive the phrases, translates, answers and scores.
def report(phrases, translate, answers, final_score):
    os.system(CLEAR)
    for x in range(0, len(phrases)):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n',
              'Phrase ', x+1, ': ', phrases[x], '\n',
              'Translate: ', translate[x], '\n',
              'You say: ', answers[x], '\n',
              'Score: ', int(final_score[x]),
              '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Your final score: ', int(sum(final_score) / len(final_score)))
    # Write the results on file.
    with open(PATH_REPORT, 'a', encoding='utf8') as file:
        if file is None:
            print("Error opening report file.")
            return
        for x in range(0, len(phrases)):
            content = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'\
                      'Phrase {}: {}\n'\
                      'Translate: {}\n'\
                      'You say: {}\n'\
                      'Score: {}\n'\
                      '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'\
                      .format(x+1, phrases[x], translate[x], answers[x], + int(final_score[x]))
            file.write(content)
        content = 'You say {} phrases and your Final Score is: {}\n'\
                  .format(len(phrases), int(sum(final_score) / len(final_score)))
        file.write(content)


# Mode that the user can talk randomly.
# Receive microphone activation time.
def free_mode(time):
    os.system(CLEAR)
    while True:
        text = get_audio(time)
        if text == 0:
            break
        else:
            print('You say: ', text)
            input('Press any key for continue!')


# Mode that the user trains with phrases.
# Receive file path.
def phrase_mode(path, time):
    answers = []
    phrases, translate = get_phrases(path)

    for x in range(0, len(phrases)):
        os.system(CLEAR)
        print('Say: ', phrases[x], '        Tradução: ', translate[x])
        text = get_audio(time)
        if text is None:
            text = ''
        answers.append(text)
        input('Press any key for continue!')

    accuracy(phrases, translate, answers)


def main():
    choice = menu()
    if choice == 0:
        free_mode(TIME_FREE)
    elif choice == 1:
        phrase_mode(PATH_BEGINNER, TIME_BEGINNER)
    elif choice == 2:
        phrase_mode(PATH_INTERMEDIATE, TIME_INTERMEDIATE)
    elif choice == 3:
        phrase_mode(PATH_ADVANCED, TIME_ADVANCED)
    elif choice == 4:
        phrase_mode(PATH_CATCH_PHRASES, TIME_CATCH_PHRASES)
    elif choice == 5:
        phrase_mode(PATH_MOVIES_SERIES, TIME_MOVIES_SERIES)


main()
