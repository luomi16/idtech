# Guess the Word Game
import random

# List of words to choose from
words = ["python", "computer", "science", "coding", "keyboard", "program", "game", "guess"]

# Select a random word from the list
word_to_guess = random.choice(words)

# Variables to track game state
guessed_letters = []
attempts_remaining = 6
word_guessed = False

print("Welcome to the Guess the Word Game!")
print(f"You have {attempts_remaining} incorrect guesses. Let's start!")

# Main game loop
while attempts_remaining > 0 and not word_guessed:
    # Display current status of guessed word
    display_word = ""
    for letter in word_to_guess:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    print(f"\nWord: {display_word}")

    # Get user's guess
    guess = input("Guess a letter: ").lower()

    # Check if user input is valid
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    # Check if letter was already guessed
    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    # Add guess to list
    guessed_letters.append(guess)

    # Check guess correctness
    if guess in word_to_guess:
        print("Correct guess!")
    else:
        attempts_remaining -= 1
        print(f"Incorrect guess! You have {attempts_remaining} guesses left.")

    # Check if the whole word has been guessed
    word_guessed = all(letter in guessed_letters for letter in word_to_guess)

# Game over conditions
if word_guessed:
    print(f"\nCongratulations! You guessed the word: '{word_to_guess}' 🎉")
else:
    print(f"\nGame Over! You're out of guesses. The word was: '{word_to_guess}'")

