# Import library for selecting a random word
# There are some very uncommon words in here, might want to creat your own list
from random_word import RandomWords

def play():
    # Select a random word
    word = RandomWords().get_random_word()

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
        print(f"YOU WIN! You correctly guessed {word.upper()}")
    else:
        print(f"YOU LOSE! The random word was {word.upper()}")

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

#play()

# NOTES FOR V2
# Add definition lookup for the words at the end of the game
# Add difficulty settings, word length, word complexity, etc.
# Add support for different lanugages
# Add "Would you like to play again?" functionality
# Adjust print out for more traditional hangman art