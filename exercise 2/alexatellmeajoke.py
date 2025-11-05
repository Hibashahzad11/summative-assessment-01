import random
import os
                #displaying a welcome banner
print("**************************************************")
print("*                                                *")
print("*           WELCOME TO MY PROGRAM🌸              *")
print("*                                                *")
print("**************************************************")
                   #path to the jokes file
JOKES_FILE = "randomjokes.txt"            
                    # function to load jokes 
def load_jokes(path):
                    #checking if the file exists      
    if not os.path.exists(path):
                    #if file not found it will display a message File not found     
        print("File not found:", path)
                    #returning an empty list   
        return []
                    #reading file content
    with open(path, "r", encoding="utf-8") as file_handler:
        content = file_handler.read().strip()
                    #taking jokes from the file 
    jokes = []
                    #splitting content into lines       
    for line in content.splitlines():
                    #skipping empty lines        
        if not line.strip():
                    #continue 
            continue 
                    #checking if the line contains a question mark
        if "?" in line: 
            setup, punch = line.split("?", 1) 
                    #adding setup to the list
            jokes.append((setup.strip(), punch.strip())) 
        else: 
                    #adding line to the list
            jokes.append((line.strip(), ""))
                   #returning the list of jokes
    return jokes 
                   #function to tell a random joke
def tell_random_joke(jokes): 
                   #choosing random joke from the list 
    setup, punch = random.choice(jokes)
                   #printing the setup of the joke 
    print("\n" + setup) 
                   #waiting for the user to input 
    input("Press Enter to see the punchline...") 
                   #printing the punchline of the joke 
    print(punch) 
                   #main function 
def main(): 
                   #loading jokes from the file
    jokes = load_jokes(JOKES_FILE)  
                   #checking if there are no jokes 
    if not jokes:
        print("No jokes found.") 
                   #terminating the program
        return 
    print("Type: ALEXA TELL ME A JOKE OR TYPE 'QUIT' TO EXIT")
                   #infinite loop to keep program running
    while True:
                   #taking user input and converting it into lowercase 
        cmd = input("\n> ").strip().lower() 
                   #checking if user wants to quit 
        if cmd in ("quit", "exit", "q"):
            print("goodBye🌸!") 
                   #breaking the loop  
            break
                   #checking if user wants to hear a joke again 
        elif "alexa" in cmd and "tell" in cmd and "joke" in cmd:
                   #telling a random joke
            tell_random_joke(jokes)
        else: 
                   #prompting user to give correct input
            print("Say 'Alexa tell me a joke' or type 'quit'.") 
                   #running the main function
if __name__ == "__main__": 
    main() 