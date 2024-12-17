def guess_number():
    print("Think of a number between 1 and 1000!")
    low, high = 1, 1000
    attempts = 0

    while low <= high:
        attempts += 1
        guess = (low + high) // 2  # Middle of the range
        answer = input(f"Is your number bigger than {guess}? (y/n): ").strip().lower()

        if answer == "y":
            low = guess + 1  # Number is greater, narrow the range
        elif answer == "n":
            high = guess - 1  # Number is less or equal, narrow the range
        else:
            print("Please answer with 'y' for yes or 'n' for no.")
            continue

    print(f"I guessed your number in {attempts} attempts! It's {low}.")

guess_number()
