import random
import string

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper functions
# -----------------------------------

def load_words():
    print("Loading word list from file...")
    with open(WORDLIST_FILENAME, 'r') as inFile:
        line = inFile.readline()
        wordlist = line.split()
    print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    return random.choice(wordlist)

wordlist = load_words()

# -----------------------------------
# Helper Functions
# -----------------------------------

def is_word_guessed(secret_word, letters_guessed):
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    guessed = ""
    for letter in secret_word:
        if letter in letters_guessed:
            guessed += letter
        else:
            guessed += "_ "
    return guessed.strip()


def get_available_letters(letters_guessed):
    available = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available += letter
    return available


# -----------------------------------
# Hint Helper Functions
# -----------------------------------

def match_with_gaps(my_word, other_word):
    # Remove spaces ( "_ p p _ e" -> "_pp_e" )
    my_word = my_word.replace(" ", "")

    # Words must be same length
    if len(my_word) != len(other_word):
        return False

    for i in range(len(my_word)):
        # If letter is revealed, it must match exactly
        if my_word[i] != "_":
            if my_word[i] != other_word[i]:
                return False
        else:
            # Blank spaces cannot contain letters
            # that already appear elsewhere in revealed pattern
            if other_word[i] in my_word:
                return False

    return True


def show_possible_matches(my_word):
    matches = []

    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)

    if len(matches) == 0:
        print("No matches found")
    else:
        print("Possible word matches are:")
        print(" ".join(matches))


# -----------------------------------
# Hangman Game
# -----------------------------------

def hangman(secret_word):

    guesses_remaining = 6
    warnings_remaining = 3
    hints_remaining = 1
    letters_guessed = []

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("-------------")

    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):

        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))

        guess = input("Please guess a letter: ").lower()

        # ---------------- HINT ----------------
        if guess == "*":
            if hints_remaining > 0:
                hints_remaining -= 1
                current_pattern = get_guessed_word(secret_word, letters_guessed)
                show_possible_matches(current_pattern)
            else:
                print("Sorry, you have already used your hint.")
            print("-------------")
            continue

        # INVALID INPUT
        if not guess.isalpha() or len(guess) != 1:
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! That is not a valid letter.")
                print("You have", warnings_remaining, "warnings left.")
            else:
                guesses_remaining -= 1
                print("Oops! That is not a valid letter.")
                print("You have no warnings left so you lose one guess.")
            print("-------------")
            continue

        # REPEATED LETTER
        if guess in letters_guessed:
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! You've already guessed that letter.")
                print("You have", warnings_remaining, "warnings left.")
            else:
                guesses_remaining -= 1
                print("Oops! You've already guessed that letter.")
                print("You have no warnings left so you lose one guess.")
            print("-------------")
            continue

        # Add valid guess
        letters_guessed.append(guess)

        # CORRECT GUESS
        if guess in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))

        # INCORRECT GUESS
        else:
            if guess in "aeiou":
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1

            print("Oops! That letter is not in my word:",
                  get_guessed_word(secret_word, letters_guessed))

        print("-------------")

    # GAME END
    if is_word_guessed(secret_word, letters_guessed):
        score = guesses_remaining * len(set(secret_word))
        print("Congratulations, you won!")
        print("Your total score for this game is:", score)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)


# -----------------------------------
# Run Game
# -----------------------------------

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)
