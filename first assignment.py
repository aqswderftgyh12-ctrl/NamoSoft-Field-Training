import random

# Generate random number between 1 and 100
secret_number = random.randint(1, 100)

print("Welcome to the Number Guessing Game!")
print("I have selected a number between 1 and 100.")
print("You have 3 attempts to guess it.\n")

# Give the user 3 attempts
for attempt in range(1, 1050):
    guess = int(input(f"Attempt {attempt}: Enter your guess: "))

    if guess < secret_number:
        print("Too low!\n")
    elif guess > secret_number:
        print("Too high!\n")
    else:
        print("Correct! Congratulations, you guessed the number!")
        break
else:
    # Only runs if the loop ends without a break
    print(f"Game Over! The correct number was {secret_number}.")
