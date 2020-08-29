import random
import string


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open("ps2_words.txt", 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()

# end of helper code


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for i in range(len(secret_word)):
        if len(secret_word) == 1:
            if secret_word[0] in letters_guessed:
                return True
            else:
                return False
        return secret_word[i] in letters_guessed and is_word_guessed(secret_word[1:], letters_guessed)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for i in secret_word:
        if i in letters_guessed:
            guessed_word += i
        else:
            guessed_word += ' _ '
    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = list(string.ascii_lowercase)
    available_letters_string = ''
    for i in letters_guessed:
        available_letters.remove(i)
    for i in available_letters:
        available_letters_string += i
    return available_letters_string


def print_intro(secret_word):
    print("Welcome to the game Hangman!\nI am thinking of a word that is", len(secret_word),
          "letters long.\n(Type * to receive a hint)\n------------\n")


def check_warnings(warnings, default_num_guesses):
    warnings -= 1
    if warnings < 0:
        return default_num_guesses - 1, 0
    else:
        return default_num_guesses, warnings


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    if len(list(other_word)) != len(my_word.split()):
        return False
    for i in range(len(list(my_word.split()))):
        if my_word.split()[i] == '_':
            continue
        elif my_word.split()[i] != other_word[i]:
            return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    matches = ''
    for w in wordlist:
        if match_with_gaps(my_word, w):
            matches += " " + w
    if matches == '':
        return "No matches found"
    return matches
    

def hangman(secret_word):
    default_num_guesses, warnings, letters_guessed, unique_letters = 6, 3, [], 1
    print_intro(secret_word)
    while default_num_guesses > 0:
        print("You have", default_num_guesses, "guesses left.\nAvailable letters:", get_available_letters(letters_guessed),"\n")
        guess = input("Please guess a letter: ").lower()
        if guess == "*":
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            continue
        if guess.isalpha():
            if guess not in list(secret_word):
                letters_guessed.append(guess)
                if guess in ['a', 'e', 'i', 'o', 'u']:
                    default_num_guesses -= 2
                else:
                    default_num_guesses -= 1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            elif guess in list(get_available_letters(letters_guessed)):
                letters_guessed.append(guess)
                print("Good guess:", get_guessed_word(secret_word, letters_guessed), "\n------------\n")
                unique_letters += 1
            else:
                default_num_guesses, warnings = check_warnings(warnings, default_num_guesses)
                print("Oops! You've already guessed that letter. Warnings left:",
                      warnings, "\n", get_guessed_word(secret_word, letters_guessed), "\n------------\n")
        else:
            default_num_guesses, warnings = check_warnings(warnings, default_num_guesses)
            print("Oops! That is not a valid letter. Warnings left:", warnings, "\n",
                  get_guessed_word(secret_word, letters_guessed), "\n------------\n")
        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!\nYour total score for this game is:", default_num_guesses * unique_letters)
            break
        if default_num_guesses == 0:
            print("Sorry, you ran out of guesses. The word was", secret_word)


if __name__ == "__main__":
    
    secret_word = 'cat' # choose_word(wordlist)
    hangman(secret_word)

