import random


def generate_mad_lib(adjective, noun, verb):
    story = "The " + adjective + " " + noun + " " + verb + " through the park."
    return story


def guessing_game():
    secret_number = random.randint(1, 100)
    guess = 0

    while guess != secret_number:
        guess = int(input("Guess a number from 1 to 100: "))

        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print("Correct! You won!")


if __name__ == "__main__":
    guessing_game()
