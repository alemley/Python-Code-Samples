from random import randint
io_control = 0
input_file = []
guessed = str()
word = []
lives = 3
letter_bank = []

print("Enter the name of the text file to use as input, including the .txt:")
while io_control == 0:
    try:
        filename = input()
        input_file = open(filename)
        io_control = 1
    except IOError:
        print("Specified file does not exist, enter a different text file:")

file_lines = []
num_lines = 0
for line in input_file:
    line = line.replace(",", " ")
    line = line.split()
    num_lines += 1
    if line:
        line = [i for i in line]
        file_lines.append(line)
i = randint(0, num_lines)
word.append(file_lines[i][0])
word.append(file_lines[i][1])

word = [item.lower() for item in word]
word = " ".join(word)

print(word)


def haswon(word, guessed_letters):
    spaces = 0
    for j in range(0, len(word)):
        if guessed_letters[j] == "_":
            spaces += 1
    if spaces == 0:
        return True
    else:
        return False


def correct(current_guess):
    if current_guess in word:
        if guess not in guessed:
            print("Correct")
            return True
    else:
        if current_guess not in word and len(guess) == 1 and str.isalpha(guess):
            if current_guess not in guessed:
                print("Letter not found.")
                return False

guessed_letters = len(word) * ['_']
print(' '.join(guessed_letters))
while lives > 0:
    guess = str(input("Guess a letter!"))
    if len(guess) != 1 or not str.isalpha(guess):
        print("Invalid input, try again.")
    if guess in guessed:
        print("Letter already guessed, try again.")
    found = correct(guess)
    guessed = guessed, guess
    if found:
        for position, letter in enumerate(word):
            if letter == guess:
                guessed_letters[position] = letter
        print(' '.join(guessed_letters))
        letter_bank.append(guess)
        print(letter_bank)
    if not found:
        print("The word does not contain this letter")
        lives -= 1
        print("You have", lives, "guesses left.")
        letter_bank.append(guess)
        print(letter_bank)
    if lives == 0 or haswon(word, guessed_letters) is True:
        if haswon(word, guessed_letters) is True:
            print("You win!!")
        else:
            print("You lose!!")
        replay = str(input("Press r to retry, or any other key to exit."))
        if replay == 1:
            break
        else:
            quit()
