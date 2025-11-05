                 # math quiz game
import random
                 #welcome message 
print(r"""
 __        __   _                             
 \ \      / /__| | ___ ___  _ __ ___   ___   
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \   
   \ V  V /  __/ | (_| (_) | | | | | |  __/   
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  

             WELCOME TO MY PROGRAM!
""")
print("Good luck!")
                 # displaying the menu
def displayMenu():
                 # difficulty level 
    print("\nDIFFICULTY LEVEL")
                 # easy level
    print(" 1. Easy (1-digit)") 
                 # moderate level 
    print(" 2. Moderate (2-digit)")
                 # difficult level 
    print(" 3. Advanced (4-digit)")
    while True:
                #letting user choose difficulty 
        choice = input("Choose difficulty (1-3): ").strip() 
                # Check if the choice is valid
        if choice in ("1","2","3"): 
                #return difficulty level
            return int(choice) 
        print("Invalid choice. Enter 1, 2 or 3.") 
                # generating random integers based on difficulty level 
def randomInt(difficulty): #generating random integers based on difficulty level 
    if difficulty == 1: #1-digit 
        return random.randint(0, 9)
    if difficulty == 2: #2-digit 
        return random.randint(10, 99)
    if difficulty == 3: #3-digit 
        return random.randint(100, 999)
                # deciding operations
def decideOperation():
               #randomly choosing options
    return random.choice(['+', '-'])
               #displaying the problem and getting user answer
def displayProblem(a, b, op): 
               #prompt for user input 
    prompt = f"{a} {op} {b} = "
               #loop until a valid integer is entered 
    while True: 
               #getting user answer
        ans = input(prompt).strip()  
               #trying to convert answer to integer 
        try:
               #returning user answer as integer 
            return int(ans) 
               #if conversion fails 
        except ValueError: 
            print("Please enter an integer answer.")
                # checking if the answer is correct 
def isCorrect(user_ans, a, b, op):
    correct = a + b if op == '+' else a - b
    return user_ans == correct, correct
               # displaying results 
def displayResults(score):
    print("\n--- Results ---")
    print(f"Your score: {score} / 100")
    pct = score
    if pct >= 90:
        grade = "A+" 
    elif pct >= 80:
        grade = "A"
    elif pct >= 70:
        grade = "B"
    elif pct >= 60:
        grade = "C"
    elif pct >= 50:
        grade = "D"
    else:
        grade = "F"
                #displaying grade
    print(f"Grade: {grade}") 
               # main quiz function 
def play_quiz(): 
    difficulty = displayMenu()
    score = 0
               #total 10 questions
    questions = 10
               #looping through questions 
    for q in range(1, questions+1): 
        a = randomInt(difficulty) # generating first random integer 
        b = randomInt(difficulty) # generating second random integer
        op = decideOperation() # deciding operation 
        print(f"\nQuestion {q} of {questions}:") #displaying question number 
               # First attempt
        user_ans1 = displayProblem(a, b, op)
              #checking answer 
        correct1, correct_val = isCorrect(user_ans1, a, b, op) 
               #if first attempt is correct 
        if correct1: 
            print("Correct! (+10)") 
            score += 10
            continue
        else:
              #prompting for second attempt 
            print("Incorrect. Try one more time.") 
                # Second attempt
            user_ans2 = displayProblem(a, b, op) 
            correct2, _ = isCorrect(user_ans2, a, b, op)
                #if second attempt is correct 
            if correct2:
                print("Correct on second attempt! (+5)")
                score += 5
            else:
                print(f"Incorrect. The correct answer was {correct_val}.")
    displayResults(score)
                # main function 
def main():
    print("Welcome to the Maths Quiz!")
                #loop to play again 
    while True:
        play_quiz()
               #asking user to play again 
        again = input("\nPlay again? (y/n): ").strip().lower() 
               #if user does not want to play again 
        if again != 'y':
               #exiting the quiz
            print("Thanks for playing goodbye!🌸") 
            break
if __name__ == "__main__":
    main()
