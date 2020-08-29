# 6.0001 Problem Set 3
# The 6.0001 Word Game

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz*'
CONSONANTSB = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# ------------  Helper code  -----------------------

WORDLIST_FILENAME = "ps3_words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    sequence: string or list
    return: dictionary
    """
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# Make sure you understand how this function works and what it does!
def display_hand(hand):
    """
    Displays the letters currently in the hand.
    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.
    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


# -------------  (end of helper code)  ----------------------


def get_word_score(word: str, n):
    score1 = 0
    word.lower()
    for let in word:
        if let == '*':
            continue
        score1 += SCRABBLE_LETTER_VALUES[let]
    score2 = 7 * len(word) - 3 * (n - len(word))
    if score2 < 1:
        score2 = 1
    return score1 * score2


# You will need to modify this for Problem #4.
def deal_hand(n) -> dict:
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.
    """
    hand = {}
    num_vowels = int(math.ceil(n / 3))
    for i in range(0, num_vowels-1, 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    hand['*'] = 1
    for i in range(num_vowels, n):
        x = random.choice(CONSONANTSB)
        hand[x] = hand.get(x, 0) + 1
    return hand


# Problem #2: Update a hand by removing letters
def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    Has no side effects: does not modify hand.
    """
    new_hand = hand.copy()
    for i in word:
        if new_hand.get(i, 0) != 0:
            new_hand[i] -= 1
    return new_hand


# Problem #3: Test word validity
def is_valid_word(word, hand, word_list) -> bool:
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    """
    copy_hand = hand.copy()
    # If letter not in hand or value is 0 (ie. used too many times), return False immediately. Otherwise, assumed True
    word = word.lower()
    for char in word:
        if copy_hand.get(char, False) is False or copy_hand.get(char, False) == 0:
            return False
        copy_hand[char] -= 1
    # Check for wildcard possibilities
    if word.find('*') != -1:
        as_list = list(word)
        new_word = ''
        for char in VOWELS:
            new_word = ''
            as_list[word.find('*')] = char
            for char in as_list:
                new_word += char
            if new_word in word_list:
                return True
        return False  # If no wildcard possibility is valid
    return word in word_list  # If no wildcard and all chars in hand, check if word is valid.



# Problem #5: Playing a hand
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for k in hand:
        length += hand[k]
    return length


def enum(string):
    switch = {
        "Yes": True,
        "yes": True,
        "y": True,
        "YES": True,
        "No": False,
        "no": False,
        "NO": False,
        "n": False,
    }
    if string in switch.keys():
        return switch[string]
    else:
        return None


def play_hand(hand, word_list):
    hand_score = 0
    re_dealt_hand = False
    re_dealt_hand_sub = False
    quitting = False
    let_subbed = False

    # Single hand
    while sum(hand.values()) > 0:

        print()
        print('Your hand:', end=' ')
        display_hand(hand)

        # Re-deal hand?
        if re_dealt_hand is False:
            ask = enum(input('\nWould you like to RE-DEAL this hand? (Only once per game!) '))
            if ask is None:
                print('I didn\'t understand. We\'re going with this one. I won\'t ask again.')
                re_dealt_hand = True
                print('Current hand:', end=' ')
                display_hand(hand)
            elif ask is False:
                print("\nOk, let's continue then...\n")
                print('Current hand:', end=' ')
                display_hand(hand)
            else:
                hand = deal_hand(HAND_SIZE)
                re_dealt_hand = True
                re_dealt_hand_sub = True
                print()
                print('Ok, new hand:', end=' ')
                display_hand(hand)

        # Substitute letter?
        if let_subbed is False:
            if re_dealt_hand_sub is False:
                ask_sub = enum(input('\nWould you like to substitute a letter? '))
                if ask_sub is None:
                    print('I didn\'t understand. Nevermind.')
                elif ask_sub is False:
                    print("Ok.")
                else:
                    ltr_choice = input('Which letter? ')
                    hand = substitute_hand(hand, ltr_choice)
                    let_subbed = True
                    print('\nLetter substituted:', end=' ')
                    display_hand(hand)

        # Okay the actual game
        guess = input('Enter word, or "!!" to indicate that you are finished with this round: ')
        if guess == '!!':
            for key in hand:
                hand[key] = 0
            quitting = True
            break
        if is_valid_word(guess, hand, word_list):
            word_score = get_word_score(guess, calculate_handlen(hand))
            hand_score += word_score
            print('"'+guess+'" ', 'earned', word_score, 'points. Score this hand:', hand_score)
        else:
            print('That is not a valid word. Please choose another word.')
        hand = update_hand(hand, guess)
        print()
    if sum(hand.values()) == 0 and quitting is False:
        print('Ran out of letters.', end=' ')
    return hand_score


# Problem #6: Playing a game
def substitute_hand(hand: dict, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    """
    del_letter = letter.lower()
    if del_letter not in hand.keys():
        return hand
    new_hand = hand.copy()
    char_list = list(string.ascii_lowercase + '*')
    for key in new_hand:
        char_list.remove(key)
    new_letter = random.choice(char_list)
    new_hand[new_letter] = new_hand[del_letter]
    new_hand[del_letter] = 0
    return new_hand


def play_game(word_list):
    hands_desired = int(input('How many hands would you like to play? '))
    total_score = 0
    for hand in range(hands_desired):
        total_score += play_hand(deal_hand(HAND_SIZE), word_list)
    return total_score



if __name__ == '__main__':
    print('\n\nThanks for playing! Your final score is:', play_game(load_words()))
