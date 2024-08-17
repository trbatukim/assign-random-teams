#reqs
import os
import random
from gtts import gTTS
from termcolor import colored
import keyboard

#Clean screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
#Flush the input stream
def flush_input():
    try:
        import msvcrt   #for Windows
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for Linux/unix/macOS
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

#Setting up necessary variables
names = []
team_names= []
team_names_bool = False
colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "light_grey", "dark_grey", "light_red", "light_green", "light_yellow", "light_blue", "light_magenta", "light_cyan"]

#Asking the user the amount of players and teams
player_num = int(input("How many players?\n"))
clear_console()
team_num = int(input("How many teams?\n"))
clear_console()

#Checking the validity of the numbers given
if (player_num < team_num):
    print("Error: The number of teams cannot be higher than the number of players. Exiting.")
    exit()

#Getting the players' names
for i in range(player_num):
    names_text = f"Name of player {i + 1}?\n"
    names.append(input(names_text))
    clear_console()

print("Will you give specific names to the teams? Y/N\n")
while True:
    if (keyboard.is_pressed("y")):
        clear_console()
        team_names_bool = True     
        flush_input()
        for i in range(team_num):
            team_names.append(input(f"Name of team {i + 1}?\n"))
            clear_console()
        break
    elif (keyboard.is_pressed("n")):
        flush_input()
        for i in range(team_num):
            team_names.append(f"{i + 1}. Team")
        break
clear_console()

#The code is put in a function so that it can be recursive
def actualCode():
    #Need to set teams_TTS here or else gets UnboundLocalError
    teams_TTS = ""
    
    #Shuffling the names so that the teams are random
    random.shuffle(names)

    #Array splitting function I got from ChatGPT
    def split(lst, n):
        k, m = divmod(len(lst), n)
        return (lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    #Splitting into teams
    team_splits = list(split(names, team_num))

    #Producing different TTS results based on whether or not the user has named the teams and printing the teams onto the terminal
    if (team_names_bool):
        for i in range(len(team_splits)):
            teams_TTS += f"Players of the team named {team_names[i]}: {team_splits[i]}, "
            print(f"{colored(team_names[i], random.choice(colors))}: {team_splits[i]}")
    else:
        for i in range(len(team_splits)):
            teams_TTS += f"Team {i + 1}: {team_splits[i]}, "
            print(f"{colored(team_names[i], random.choice(colors))}: {team_splits[i]}")

    #Creating and playing TTS
    save_dir = os.path.join(os.getcwd(), "teams.mp3")
    os.makedirs(save_dir, exist_ok=True)
    tts = gTTS(text=teams_TTS, lang="en", tld="us", slow=False)
    save_dir = os.path.join(save_dir, "teams.mp3")
    tts.save(save_dir)
    os.system(f"start {save_dir}")
    
    #Asking the user if they want to shuffle again and reexecute the code depending on their answer
    print("Scramble teams? Y/N\n")    
    while True:
        if (keyboard.is_pressed("y")):
            clear_console()
            actualCode()
            break
        elif (keyboard.is_pressed("n")):
            clear_console()
            os.remove(save_dir) #Removing the mp3 file before exiting
            exit()

actualCode()