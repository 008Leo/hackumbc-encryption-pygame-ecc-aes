
# importing external files and functions.

import sys
import random

# Code mention in document.
if len(sys.argv) >= 2:
    seed(sys.argv[1])
if __name__ == "__main__":
    # A variable to count the number of times we try to guess that number.
    loop = 0
    # A boolean variable for the while loop.
    Anything = True
    # Using the random function to use a random number between 1 to 100.
    starting_num = int(input("enter a starting number: "))
    ending_num = int(input("enter a ending number: "))

    number = random.randint(starting_num, ending_num)



    # The while loop.
    while Anything:
        # looping the input function until the user guesses the number.
        guess = int(input(f"Guess a number between {starting_num} to {ending_num}: "))

        # An if-statement to ensure we are entering a number between 1 and 100.
        if guess < starting_num or guess > ending_num:
            print(f"enter a number between {starting_num} to {ending_num}")
        else:
            if guess > number:
                # If your guess is higher than the actual number.
                print("your guess is too high")
                loop += 1
            elif guess < number:
                # If your guess is lower than the actual number.
                print("your guess is too low")
                loop += 1
            elif guess == number:
                # If your guess is equal to the actual number.
                # And the loop increments by 1 as you have more tries.
                loop += 1
                print(f"You guessed the number! It took you {loop} steps.")
                # we stop the while loop here.
                Anything = False
