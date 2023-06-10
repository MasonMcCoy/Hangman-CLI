# Import library for selecting a random word
# There are some very uncommon words in here, might want to creat your own list
from random_word import RandomWords
import requests
from config import API_KEY

def play():
    # Select a valid random word and look up its details
    wordDict = getRandomWord()

    # Our random word
    word = wordDict["word"]

    # Our random word's type, etymology, usage date, and short definition
    details = wordDict["info"]

    # Create a list of our random word's characters
    wordChars = list(word)

    # Create a mirrored list of blanks that match our list of random word characters
    playerChars = ["_"] * len(word)

    # Create an empty set for player guesses to be added to
    badGuesses = set()

    # Set number of guesses allowed before a loss condition
    badGuessRem = 5

    # Instantiates player turn count
    playerTurn = 1

    # Sets win condition to False by default
    gameWin = False

    # The game will continue until player has exhausted incorrect guess allowance or the word characters are correctly guessed
    while badGuessRem > 0 and gameWin is False:
        # Display blank list of characters to the player
        print(playerChars)

        # Logic to more cleanly display incorrect guesses made by the player
        if len(badGuesses) < 1:
            print("Incorrect Guesses: None")
        else:
            print(f"Incorrect Guesses: {badGuesses}")

        # Call guess function and appropriately set remaining incorrect guesses allowed
        badGuessRem = guess(wordChars, playerChars, badGuesses, badGuessRem, playerTurn)

        gameWin = isGameWon(wordChars, playerChars)
        # Increment player turn after player's input has been recieved and processed
        playerTurn += 1

        # Displays remaining incorrect guesses allowed
        print(f"Remaining Guesses: {badGuessRem}")
        print("\n")

    # Logic to display win/lose message
    if gameWin is True:
        print(f"YOU WIN! You correctly guessed {word.upper()}.\n")
    else:
        print(f"YOU LOSE! The random word was {word.upper()}.\n")

    # Display info about our random word via API call
    displayWordInfo(word, details["type"], details["etymology"], details["date"], details["definition"])

# Uses RandomWords library to find a random English word with a valid definition
def getRandomWord():
    # Select English word at random (not all words seems to be valid)
    word = RandomWords().get_random_word()
    print("Finding random word...")

    # Gather information about our random word, or select a new word if word is invalid
    try:
        wordInfo = getWordInfo(word)
    except:
        return getRandomWord()
    
    # New dictionary for word and word information
    wordDict = {
        "word": word,
        "info": wordInfo
    }

    return wordDict

# Utilizes Merriam-Webster's dictionary API to gather information about a given word
def getWordInfo(word):
    # Make API call with provided word
    r = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={API_KEY}")

    # TO-DO: Allow for user to iterate through potential meanings
    # Word type, i.e. verb, noun, etc.
    type = r.json()[0]['fl']

    # Word etymology, should it be available
    try:
        etymology = r.json()[0]['et']
    except:
        etymology = "No available etymology"
    
    # Date of first known usage of the word, if available
    try:
        date = r.json()[0]['date']
    except:
        date = "No available date"
    
    # TO-DO: Iterate through all provided definitions
    # Word short definition, provided as a list
    definition = r.json()[0]['shortdef'][0]
    
    # New dictionary of word information
    wordInfo = {
        "type": type,
        "etymology": etymology,
        "date": date,
        "definition": definition
        }
    
    return wordInfo

# Display formatted word information to player
def displayWordInfo(word, wordType, wordEt, wordDate, wordDef):
    print(f"{word}, {wordType}\nEtymology: {wordEt}\nFirst Used: {wordDate}\n{wordDef}\n")

# Allows player to make a guess, checks to see if guess is valid
def guess(wordChars, playerChars, badGuesses, badGuessRem, playerTurn):
    while True:
        # Player input with iterating turn count
        currGuess = input(f"Guess {playerTurn}: ")

        try:
            # Determines if player input is an alphabetical chacter, raises exception otherwise
            if currGuess.isalpha():
                currGuess = currGuess.lower()
            else:
                # Raising a generic exception like this should be avoided, but should be fine in this particular case
                raise Exception
        except:
            print("Please enter valid characters only.")
            continue

        # Checks length of player input and rejects if 1+ characters
        if len(currGuess) > 1:
            print("Please only enter 1 character.")
            continue

        break

    # Checks if player input is already among prevoius guesses and rejects input if so
    if currGuess in  playerChars:
        print(f"You've already guessed {currGuess}!")
        return guess(wordChars, playerChars, badGuesses, badGuessRem, playerTurn)
    
    # Calls function to determine if guess is in our random word
    else:
        return charInWord(currGuess, wordChars, playerChars, badGuesses, badGuessRem)

# Function to determine if player guess is in our random word
def charInWord(char, wordChars, playerChars, badGuesses, remainingGuesses):
    # Determines if guessed character is in the list of our word's characters
    if char in wordChars:
        # Identifies the indices of all occurences of the character
        charPositions = [i for i, j in enumerate(wordChars) if j == char]

        # Updates the player's instance of the character list with correct guesses
        for x in charPositions:
            playerChars[x] = char
    
    else:
        # Adds the incorrect guess to the set of bad guesses
        badGuesses.add(char)

        # Decrements the amount of remaining guesses by 1
        remainingGuesses -= 1

        # Print statement sharing the incorrect guess with the player
        print(f"{char} is not in the word!")

    # Returns the amount of remaining guesses
    return remainingGuesses

def isGameWon(wordChars, playerChars):
    if wordChars == playerChars:
        gameWon = True
    else:
        gameWon = False
    return gameWon

play()

# NOTES FOR V2
# Add definition lookup for the words at the end of the game X
# Add difficulty settings, word length, word complexity, etc.
# Add support for different lanugages
# Add "Would you like to play again?" functionality