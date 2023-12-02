'''
===PROJECT DETAILS===

Project Name: Mini Jeopardy: The Final Push

Developers:
    - Lead: Paolo Mayo
    - Enter your names here

Project Description:
    Insert Project Description here.


Note For Other Developers:
    When editing this code, please take note of the following:
        1. pass
'''

#############################################
# Module Imports                            #
#############################################

#Built-in
from abc import ABC, abstractmethod
import tkinter as tk
from random import choice, sample
from os import chdir
from sys import path

#External
from PIL import Image,ImageTk
from pygame import mixer

# Custom Modules
import questions
import style_sheet as ss

#############################################
# Tkinter Setup                             #
#############################################
root = tk.Tk()

# Set Attributes
root.attributes('-fullscreen', True)
root.title('Mini Jeopardy 2.0')

#############################################
# Global Variables / Setup                  #
#############################################

# Set the current working directory to the folder containing the script
chdir(path[0])

# Rendering Information
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

Images={}

# Load Image for Logo
Images['logoImage'] = tk.PhotoImage(file="Sprites/logo.png")

# Load Image for Background
background = Image.open("sprites/background.png").resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.Resampling.NEAREST)
Images['backgroundImage'] = ImageTk.PhotoImage(background, master = root)

# Load Image for Host Sprite
host = Image.open("sprites/host.png").resize((200,200), Image.Resampling.NEAREST)
Images["host"] = ImageTk.PhotoImage(host, master = root)

# Load Image for a Smaller Host Sprite
smallHost = Image.open("sprites/host.png").resize((120,120), Image.Resampling.NEAREST)
Images["small_host"] = ImageTk.PhotoImage(smallHost, master = root)

# Player 1 Icons
NP1Icon = Image.open("sprites/negative - player 1.png").resize((250,250), Image.Resampling.NEAREST)
Images['level0_player1'] = ImageTk.PhotoImage(NP1Icon, master = root)

for iconNum in range(1,4+1):
  P1Icon = Image.open(f"sprites/level {iconNum} - player 1.png").resize((250,250), Image.Resampling.NEAREST)
  Images[f'level{iconNum}_player1'] = ImageTk.PhotoImage(P1Icon, master = root)
  
# Player 2 Icons
NP2Icon = Image.open("sprites/negative - player 2.png").resize((250,250), Image.Resampling.NEAREST)
Images['level0_player2'] = ImageTk.PhotoImage(NP1Icon, master = root)

for iconNum in range(1,4+1):
  P1Icon = Image.open(f"sprites/level {iconNum} - player 2.png").resize((250,250), Image.Resampling.NEAREST)
  Images[f'level{iconNum}_player2'] = ImageTk.PhotoImage(P1Icon, master = root)


FONT = ("Euphemia", 13)
Sounds = {
  "bgm": "bgm.wav",
  "correct":["Correct answer 1.wav", "Correct answer 2.wav","Correct answer 3.wav", "Correct answer 4.wav", "Correct answer 5.wav"],
  "wrong":["Wrong answer 1.wav", "Wrong answer 2.wav", "Wrong answer 3.wav", "Wrong answer 4.wav", "Wrong answer 5.wav"],
}

# Play Background Music
mixer.init()
mixer.Channel(0).play(mixer.Sound("bgm.wav"), loops=-1)

#############################################
# Class Declarations                        #
#############################################

# Game State Data ---------------------------
class GameState():


    def __init__(self):
        self.set_actual_questions()
        self.gameDifficulty: str = "FIRST_GRADE"
        self.playerNames: list[str] = ["Player", "bot"]
        self.possibleQuestions: dict = questions.possibleQuestions
        self.isPlayerMove:bool = True


    def set_actual_questions(cls):
        '''
        loads 4 random questions per category, for 5 categories
        sets 5 questions as "golden questions": questions that allow you to steal half of your opponent's score
        from the possibleQuestions variable to actualQuestions
        ->no return value
        developer-in-charge: mayo
        '''

        possibleQuestions = questions.possibleQuestions
        
        questionList:dict= { #Edited to reflect changes with names. -Sam
            "History":[],
            "Science":[],
            "Business":[],
            "Pop Culture":[],
            }

        for category in possibleQuestions: # Loops through all the categories
            randomQuestions = sample(possibleQuestions[category], 4)    #get 4 random questions per category

            bid = 200
            for question in randomQuestions: #loops through the questions in a given category
                #Attach a bid value to the questions
                question["value"] = bid
                bid += 200

                #Set as non-golden by default
                question["isGolden"] = False

                #Attach a Flag to keep track of asked questions
                question["isAlreadyAsked"] = False

                # Sets one question in the category as golden
                choice(randomQuestions)["isGolden"] = True

            questionList[category]=(randomQuestions)   # Updates the global variable based on generated random questions

        cls.actualQuestions = questionList


# Page Classes ------------------------------
class Page(ABC):
    """
    An Abstract class that contains that defines, 
    without implementing, the needed methods for 
    all pages.

    Developer-in-Charge: Samuel Samonte

    Attributes
    ----------
    None: None
    """

    @abstractmethod
    def run():
        '''
        everything necessary for the page to run
        '''
        pass

    @abstractmethod
    def render():
        '''
        renders the associated graphics
        '''
        pass

    @abstractmethod
    def process():
        '''
        associated processes with this page
        '''
        pass

    def change_page(self, nextPage, *args):
        '''
        calls the next page and clears the output
        '''
        nextPage.run(*args)

    def clear_notebook_screen(self):
        '''
        clears the screen
        '''
        for widget in root.winfo_children():
            widget.destroy() 


class MenuPage(Page):
    '''
    displays the main menu
    developer-in-charge: samonte
    
    Attributes
    ----------
    None: None
    '''

    def run(self, gameState):
        self.render(gameState)

    def render(self, gameState):
        '''
        prints the info for the menu
        Accepts user input via buttons
        ->no return value
        developer-in-charge: Sam
        '''
        global root
        global ENVIRONMENT
        global FONT
        global Images
        
        #Display Background
        background = tk.Label(root,image = Images['backgroundImage'])
        background.place(x=0, y=0)

        #Display Logo
        photo = tk.Label(root, image=Images['logoImage'], bg = ss.COLORS["MONEY_GREEN"])
        photo.pack(pady=35)

        #Display "Choose Difficulty"
        textToShow = tk.Label(
                        text="Please Choose Difficulty",
                        font=ss.H2["FONT"],
                        fg=ss.H2["FONT_COLOR"],
                        bg=ss.H2["BACKGROUND_COLOR"],
                        )
        textToShow.pack(padx= 10, pady=10)

        #Display Difficulties
        HEIGHT = 1
        WIDTH = 60
        FirstGradeButton = tk.Button(
                            font=ss.OPTION_BUTTONS["FONT"],
                            bg =ss.OPTION_BUTTONS["BACKGROUND_COLOR"],
                            fg =ss.OPTION_BUTTONS["FONT_COLOR"],
                            master=root,
                            height=HEIGHT, width=WIDTH,
                            text="First Grader - Gets it right ~33% of the time",
                            command=lambda: self.process("FIRST_GRADER", gameState))
        HighSchoolerButton = tk.Button(
                            font=ss.OPTION_BUTTONS["FONT"],
                            bg =ss.OPTION_BUTTONS["BACKGROUND_COLOR"],
                            fg =ss.OPTION_BUTTONS["FONT_COLOR"],
                            height=HEIGHT, width=WIDTH,
                            master=root,
                            text="High Schooler - Gets it right ~60% of the time",
                            command=lambda: self.process("HIGH_SCHOOLER", gameState))
        PioneerButton = tk.Button(
                            font=ss.OPTION_BUTTONS["FONT"],
                            bg =ss.OPTION_BUTTONS["BACKGROUND_COLOR"],
                            fg =ss.OPTION_BUTTONS["FONT_COLOR"],
                            height=HEIGHT, width=WIDTH,
                            master=root,
                            text="BSDSBA BATCH 2027 STUDENT PIONEER - Gets it right ALL THE TIME",
                            command=lambda: self.process("BSDSBA_PIONEER", gameState))
        PVPButton = tk.Button(
                            font=ss.OPTION_BUTTONS["FONT"],
                            bg =ss.OPTION_BUTTONS["BACKGROUND_COLOR"],
                            fg =ss.OPTION_BUTTONS["FONT_COLOR"],
                            height=HEIGHT, width=WIDTH,
                            master=root,
                            text="PLAYER VERSUS PLAYER",
                            command=lambda: self.process("PVP", gameState))

        FirstGradeButton.pack(pady=2)
        HighSchoolerButton.pack(pady=2)
        PioneerButton.pack(pady=2)
        PVPButton.pack(pady=2)


        root.mainloop()
        mixer.quit()

    def process(self, difficulty, gameState):
        ''' 
        updates currentScene and gameDifficulty variables
        str, str -> no return value
        developer-in-charge: mayo
        '''

        #updates difficulty
        gameState.gameDifficulty = difficulty
        
        intro = IntroPage()
        self.change_page(intro, gameState)

class IntroPage(Page):
    '''
    displays the very first screen you see
    developer-in-charge: Samuel Samonte

    Attributes
    ----------
    None: None
    '''

    def run(self, gameState):
        '''
        Renders the Instructions and accepts user input if PVP
        developer-in-charge: mayo
        '''
        self.render(gameState)    # Renders the instructions to the game
        if gameState.gameDifficulty == "PVP":
            players = self.get_players_names(gameState)    # Waits for user
        else:
            startButton = tk.Button(
                                text="Start Game",
                                command = lambda: update_info_from_intro('QUESTION_SELECT', PlayerNames),
                                font=ss.PRIMARY_BUTTON["FONT"],
                                bg=ss.PRIMARY_BUTTON["BACKGROUND_COLOR"],
                                fg=ss.PRIMARY_BUTTON["FONT_COLOR"])
            startButton.pack()

    def get_players_names(self, gameState):
        '''
        Waits for user Input before allowing code execution to continue
        and gets players' names if PVP
        ->no return value
        developer-in-charge: mayo
        '''
        global root
        global FONT

        # Setup a table
        nameInputFrame = tk.Frame(root)
        nameInputFrame.columnconfigure(0, weight=1)
        nameInputFrame.columnconfigure(1, weight=1)

        #Setup prompts
        label1 = tk.Label(nameInputFrame, text="PLAYER 1 NAME: ", font=FONT)
        label1.grid(column=0, row=0)

        label2 = tk.Label(nameInputFrame, text="PLAYER 2 NAME: ", font=FONT)
        label2.grid(column=1, row=0)

        # Setup Text Fields
        Player1Input = tk.Text(nameInputFrame, height=1)
        Player2Input = tk.Text(nameInputFrame, height=1)

        Player1Input.grid(column=0, row=1)
        Player2Input.grid(column=1, row=1)
        
        #Setup Start Button
        startButton = tk.Button(
                            root, text="Start Game",
                            command= lambda:self.get_players_names_from_fields(Player1Input, Player2Input, gameState),
                            font=ss.PRIMARY_BUTTON["FONT"],
                            bg=ss.PRIMARY_BUTTON["BACKGROUND_COLOR"],
                            fg=ss.PRIMARY_BUTTON["FONT_COLOR"])

        nameInputFrame.pack(fill="x", padx=30, pady=20)
        startButton.pack(pady=30)
        
        return

    def get_players_names_from_fields(self, field1, field2, gameState):
        '''
        Gets Player Names from the tkinter textboxes and sets it to the global Player Names Variable
        textField1, textField2 -> no return value
        '''
        
        #Get Player Input
        field1Text = field1.get(1.0, "end-1c")
        field2Text = field2.get(1.0, "end-1c")

        #Check if Input is empty before putting in player input
        if field1Text != "":
            gameState.playerNames[0] = field1Text
        
        if field2Text != "":
            gameState.playerNames[1] = field2Text
        
        self.process(gameState)
        

    def render(self, gameState):
        '''
        prints the info for the intro
        accepts name as input when PVP
        ->no return value
        developer-in-charge: Chloe
        '''
        global root
        global FONT
        global scaledLogo
        global Images
        global SCREEN_HEIGHT

        # Clear Screen
        self.clear_notebook_screen()

        # Display Bacground Image
        background = tk.Label(root,image = Images['backgroundImage'])
        background.place(x=0, y=0)

        # Display Header
        header = tk.Label(
                        text= f'HOW TO PLAY:',
                        font=ss.H2["FONT"],
                        fg=ss.H2["FONT_COLOR"],
                        bg=ss.H2["BACKGROUND_COLOR"])
        header.pack(pady=SCREEN_HEIGHT/20)

        #Rules and Story Table
        table = tk.Frame(root, bg=ss.COLORS["DARK_MONEY_GREEN"])
        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=3)

        #Display Story
        storyFrame = tk.Frame(table, bg=ss.COLORS["DARK_MONEY_GREEN"])
        storyFrame.grid(column=2, row=0, sticky=tk.W+tk.E)

        story = tk.Label(
                text="You are an aspiring businessman who just opened their first store. In order to lead a successful company, you must answer a set of questions with corresponding monetary values. When you answer a question correctly, you will acquire its value which you can use to grow your business.\n\nAnother ambitious businessman has come to town in hopes of building their business here. The two businessmen must now compete in order to gain more money to boost their companies and become the leading tycoon of the city!",
                master=storyFrame,
                font = ss.REGULAR_TEXT["FONT"],
                fg=ss.COLORS["ACCENT_GOLD"],
                bg=ss.COLORS["DARK_MONEY_GREEN"],
                wraplength=600, justify="left")
        story.pack(anchor="w", padx=10, pady=1, ipady=10)

        # Display Rules
        ruleFrame = tk.Frame(table,bg=ss.COLORS["DARK_MONEY_GREEN"])
        ruleFrame.grid(column=1, row=0, sticky=tk.W)
        rules = '1. Click the "Start" button to begin the game.|2. Select the category of questions you want to answer|3. You will be presented with a question from the selected category.|4. Read the question and carefully consider the answer choices (a, b, c).|5. Click on the choice that you believe is correct.|6. Your final score will be displayed at the end of the game'.split("|")
        for rule in rules:
            textLine = tk.Label(
                            text=rule, master=ruleFrame,
                            font = ss.REGULAR_TEXT["FONT"],
                            fg=ss.REGULAR_TEXT["FONT_COLOR"],
                            bg=ss.COLORS["DARK_MONEY_GREEN"])
            textLine.pack(anchor="w", padx=10, pady=1)
        table.pack(fill="x", padx=15, pady=10)
        return 

    def process(self, gameState):
        '''
        changes scene from intro to question select
        -> no return value
        developer-in-charge: mayo
        '''

        question_select = QuestionBoardPage()
        self.change_page(question_select, gameState)


class QuestionBoardPage(Page):
    '''
    displays the board with all of the bid values
    developer-in-charge: samonte

    Attributes
    ----------
    None: None
    '''

    def run(self, gameState):
        '''
        renders the question board, selects a random question if bot's turn
        developer-in-charge: mayo
        '''
        self.render(gameState)
        if (not gameState.isPlayerMove) and (gameState.gameDifficulty!='PVP'): #If bot's move, choose a question randomly
            selectedCategory, selectedBid = get_bot_chosen_question()   # Gets the user's input for the question parameters
            root.after(1500, lambda: update_info_from_question_select('IrrelevantArg', selectedCategory, selectedBid))

    def render(self, gameState):
        '''
        prints the info for the question board
        Displays button for each question
        ->no return value
        developer-in-charge: mayo
        '''
        isPlayerMove = gameState.isPlayerMove

        categoryHeaders = ["History: 1", "Science: 2", "Business: 3", "Pop Culture: 4"]

        #FOR NOTEBOOK ENVIRONMENTS
        # Clear Screen
        self.clear_notebook_screen()

        # Display Bacground Image
        background = tk.Label(root,image = Images['backgroundImage'])
        background.place(x=0, y=0)

        # Configure Table
        nameInputFrame = tk.Frame(root, bg=ss.COLORS["DARK_MONEY_GREEN"])
        for columns in range(4):
            nameInputFrame.columnconfigure(columns, weight=1)

        # Spacer
        northPadding = tk.Frame(root)
        northPadding.pack(pady=30)

        #Display Category Names
        for columns, category in enumerate(categoryHeaders):
            categoryLabel = tk.Label(
                            nameInputFrame,text=category[:-3],
                            font=ss.H1["FONT"],
                            height=2,
                            bg=ss.H1["BACKGROUND_COLOR"],
                            fg=ss.H1["FONT_COLOR"])
        categoryLabel.grid(column=columns, row=0)

        #loop Through Categories
        for categoryNum, category in enumerate(gameState.actualQuestions):
            for questionNum, questions in enumerate(gameState.actualQuestions[category]): #loops through the questions in category
                formattedBid = "$" + str(questions["value"])
                questionSelect = tk.Button(
                                    nameInputFrame,
                                    text=formattedBid,
                                    font=ss.BID_CARD["FONT"],
                                    height=2,
                                    command= lambda catNum = (categoryNum+1)%4,
                                                    bidVal = questions["value"]:update_info_from_question_select("IrrelevantArg", catNum, bidVal),
                                    fg=ss.BID_CARD["FONT_COLOR"],
                                    bg=ss.BID_CARD["BACKGROUND_COLOR"])
            questionSelect.grid(row=questionNum+1, column=(categoryNum)%4, sticky="EW")

            if (formattedBid=="$---" or formattedBid == "$-GOLDEN-$") or ((not isPlayerMove) and (gameDifficulty!="PVP")):
                questionSelect.configure(state="disabled") #Disabled when already asked OR bot's move

        nameInputFrame.pack(fill="both", pady=5, padx=25)

        # Shows host saying whose turn it is
        prompts = ["Your Move!", "Time to shine! :>", "Choose your question! OwO", "Your Turn!", "Your Turn Pookie bear!"]
        hostFrame = tk.Frame(root, bg=ss.PRIMARY_BUTTON["BACKGROUND_COLOR"],)
        hostFrame.columnconfigure(0, weight=1)
        hostFrame.columnconfigure(1, weight=2)

        hostImage = tk.Label(hostFrame, image=Images["small_host"], bg=ss.COLORS["HIGHLIGHT_YELLOW"])
        hostImage.grid(column=0, row=0, sticky="w")

        currentContestant = "HELLO"
        if isPlayerMove:
            currentContestant = gameState.playerNames[0]
        else:
            currentContestant = gameState.playerNames[1]


        hostPrompt = tk.Label(
                        hostFrame,
                        text=f"{currentContestant}, {choice(prompts)}",
                        font=ss.PRIMARY_BUTTON["FONT"],
                        fg=ss.PRIMARY_BUTTON["FONT_COLOR"],
                        bg=ss.PRIMARY_BUTTON["BACKGROUND_COLOR"],
                        justify="left")
        hostPrompt.grid(column=1, row=0, sticky="w")


        hostFrame.pack(fill="x", padx=20, pady=20)
    
    def process(nextScene, questionCategory, questionBidValue):
        '''
        Edits the currentQuestion var to a dict containing the question details
        str, int, str -> no return value
        developer-in-charge: mayo
        '''
        global lastBidValue
        global currentQuestion
        global ENVIRONMENT

        #Update Bid Value
        lastBidValue = int(questionBidValue)

        #Get the question
        currentQuestion = get_question(questionCategory, questionBidValue)

        #Mark the question as asked
        currentQuestion["isAlreadyAsked"] = True
        if currentQuestion["isGolden"]:
            currentQuestion["value"] = "-GOLDEN-$"
        else:
            currentQuestion["value"] = "---"

        # Change Scene Based on Environment
        if ENVIRONMENT == "COLAB":
            change_scene_to(nextScene)
        else:
            do_question_showing()


class QuestionCardPage(Page):
    '''
    displays the question itself
    developer-in-charge: samonte

    Attributes
    ----------
    None: None
    '''

    def run():
        '''
        renders the question card, accepts bot move
        developer-in-charge: mayo
        '''
        render_question_card()
        if (not isPlayerMove) and (gameDifficulty!='PVP'): #If bot's move, choose an answer
            answerStatus = get_bot_answer_to_question_notebook()   # Gets the user's input for the question parameters
            root.after(1500, lambda: update_info_from_question_showing("IrrelevantArg", answerStatus))

    def render():
        '''
        prints the question and relevant parameters
        ->no return value
        developer-in-charge: Cheska
        '''
        global currentQuestion
        global lastBidValue
        global PlayerNames
        global ENVIRONMENT
        global FONT
        global actualQuestions
        global root
        global Images

        #Initializing Local Variables
        questionText = currentQuestion["Question"]
        questionChoices = currentQuestion["Choices"]
        questionForWhom = ""

        if isPlayerMove:
            questionForWhom = PlayerNames[0]
        else:
            questionForWhom = PlayerNames[1]


        if ENVIRONMENT == "COLAB":

            output.clear()

            # Prints the question, bid value, and choices with formatting
            print(f"======= {questionForWhom}: For ${lastBidValue} =======")
            print("QUESTION: ")
            print(f" {questionText}")
            print("")
            print("CHOICES: ")
            for choice in questionChoices:
                print(choice)
                print("")


        else: #FOR NOTEBOOK ENVIRONMENTS
            # Clear Screen
            clear_notebook_screen()

            # Display Bacground Image
            background = tk.Label(root,image = Images['backgroundImage'])
            background.place(x=0, y=0)

            #Display Header
            header = tk.Label(
                            text=f"======= {questionForWhom}: For ${lastBidValue} =======",
                            font = ss.H2["FONT"],
                            fg= ss.H2["FONT_COLOR"],
                            bg= ss.H2["BACKGROUND_COLOR"])
            header.pack(pady=45)

            #Display Question
            header = tk.Label(
                            text=f"{questionText}",
                            font = ss.QUESTION_CARD["FONT"],
                            wraplength=1000, height=4, padx= 30,
                            fg= ss.QUESTION_CARD["FONT_COLOR"],
                            bg= ss.QUESTION_CARD["BACKGROUND_COLOR"])
            header.pack()

            #Spacer
            spacer = tk.Label(text="", bg=ss.COLORS["MONEY_GREEN"])
            spacer.pack(pady=10)

            #Display Options
            for choice in questionChoices:
                answerButton = tk.Button(text=choice, font=(FONT[0], 20, "bold"), command=lambda answer=choice[0]: get_user_answer_to_question(answer), bg="#F5E6CA", fg="#020024")
                answerButton.pack(pady=10, fill="x")

            if (not isPlayerMove) and (gameDifficulty!="PVP"):
                answerButton.configure(state="disabled") #Disabled when bot's move

    def process(nextScene, isAnswerCorrect):
        '''
        updates the currentScore is answer is correct
        -> no return value
        developer-in-charge: mayo
        '''
        global isLastAnswerCorrect
        global currentPlayerScore
        global lastBidValue
        global current
        global isPlayerMove
        global currentBotScore
        global ENVIRONMENT

        # Updates player score
        if isPlayerMove:
         if isAnswerCorrect:
            isLastAnswerCorrect = True
            currentPlayerScore += lastBidValue
         else:
            isLastAnswerCorrect = False
            currentPlayerScore -= lastBidValue
        else:
         if isAnswerCorrect:
            isLastAnswerCorrect = True
            currentBotScore += lastBidValue
         else:
            isLastAnswerCorrect = False
            currentBotScore -= lastBidValue

        # Changes Scene based on ENVIRONMENT
        if ENVIRONMENT == "COLAB":
            change_scene_to(nextScene)
        else:
            do_score_showing()



class ScoreBoardPage(Page):
    '''
    displays the scoreboard
    developer-in-charge: samonte

    Attributes
    ----------
    None: None
    '''

    def run():
        '''
        check if there are no more questions
        show score if there are still questions, show winner otherwise
        developer-in-charge: mayo
        '''

        check_if_no_more_questions()

        render_player_score()
        if isGameOngoing:
            if currentQuestion["isGolden"]:
                goldenQuestionButton = tk.Button(root, text="Answer a Golden Question", command=lambda: update_info_from_contestants_score("GOLDEN_QUESTION_SHOWING"), font=(FONT[0], 20, "bold"),bg="#F5E6CA", fg="#020024")
                goldenQuestionButton.pack(pady=15)
            else:
                endTurnButton = tk.Button(root, text = "End Turn", command=lambda: update_info_from_contestants_score('IrrelevantArg'), font=(FONT[0], 20, "bold"),bg="#F5E6CA", fg="#020024")
                endTurnButton.pack(pady=15)
        else:
            endTurnButton = tk.Button(root, text = "End Game", command=root.destroy, font=(FONT[0], 20, "bold"),bg="#F5E6CA", fg="#020024")
            endTurnButton.pack(pady=15)

    def render():
        '''
        prints the scores of both contestants
        -> no return value
        developer-in-charge: Cheska
        '''
        global currentPlayerScore
        global previousPlayerScore
        global currentBotScore
        global previousBotScore
        global isLastAnswerCorrect
        global lastBidValue
        global isPlayerMove
        global PlayerNames
        global ENVIRONMENT
        global root
        global FONT
        global isGameOngoing
        global Images
        global Sounds



        # Text Formatting
        currentPlayerScoreAsText = format_text_to_constant_width(str(currentPlayerScore), 5)
        previousPlayerScoreAsText = format_text_to_constant_width(str(previousPlayerScore), 5)
        playerScoreDeltaAsText = format_text_to_constant_width(str(abs(currentPlayerScore - previousPlayerScore)),5)

        if currentPlayerScore - previousPlayerScore >0:
            playerScoreDeltaAsText = "+"+playerScoreDeltaAsText # NOTE: += is not applicable here because concat is not associative
        else:
            playerScoreDeltaAsText = "-"+playerScoreDeltaAsText

        currentBotScoreAsText = format_text_to_constant_width(str(currentBotScore), 5)
        previousBotScoreAsText = format_text_to_constant_width(str(previousBotScore), 5)
        botScoreDeltaAsText = format_text_to_constant_width(str((abs(currentBotScore - previousBotScore))), 5)

        if currentBotScore - previousBotScore >0:
            botScoreDeltaAsText = "+"+botScoreDeltaAsText # NOTE: += is not applicable here because concat is not associative
        else:
            botScoreDeltaAsText = "-"+botScoreDeltaAsText

        scoreOperand = "+"
        currentContestant = ""
        answerStatus = ""

        # Sets the appropriate Contestant, scoreOperand, and answer status based on
        # whose turn it is and whether the last answer was correct

        if isPlayerMove:
            currentContestant = PlayerNames[0]
        else:
            currentContestant = PlayerNames[1]

        if isLastAnswerCorrect:
            scoreOperand = "+"
            answerStatus = "got it CORRECT!"
        else:
            scoreOperand = "-"
            answerStatus = "got it WRONG!"



        if ENVIRONMENT == "COLAB":

            output.clear()

            # Prints the scoreboard
            print(
            f'''{PlayerNames[0]}     {PlayerNames[1]}
        ☻☻☻☻☻     ○○○○○
        ☻☻☻☻☻     ○○○○○
        ☻☻☻☻☻     ○○○○○
        ████████   ████████
        █ {previousPlayerScoreAsText}█   █ {previousBotScoreAsText}█
        █{playerScoreDeltaAsText}█   █{botScoreDeltaAsText}█
        █ ──── █   █ ──── █
        █ {currentPlayerScoreAsText}█   █ {currentBotScoreAsText}█
        █      █   █      █''')

            print("=======================")
            print(f"{currentContestant} {answerStatus}")

        else: #FOR NOTEBOOK ENVIRONMENTS
            DARK_GREEN = ss.COLORS["DARK_MONEY_GREEN"]

            # Clear Screen
            clear_notebook_screen()

            # Display Bacground Image
            background = tk.Label(root,image = Images['backgroundImage'])
            background.place(x=0, y=0)

            # Spacer
            northPadding = tk.Frame()
            northPadding.pack(pady=25)


            #Setup score board
            frame = tk.Frame(root, bg=ss.COLORS["HIGHLIGHT_YELLOW"])
            frame.columnconfigure(0, weight=10) # Player 1 column
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=10) # Player 2 column

            # Determines the icon sprite to be used
            iconNumPlayer1 = 4
            if currentPlayerScore<0:
                iconNumPlayer1=0
            elif currentPlayerScore<1000:
                iconNumPlayer1=1
            elif currentPlayerScore<2000:
                iconNumPlayer1=2
            elif currentPlayerScore<3000:
                iconNumPlayer1=3

            iconNumPlayer2 = 4
            if currentBotScore<0:
                iconNumPlayer2=0
            elif currentBotScore<1000:
                iconNumPlayer2=1
            elif currentBotScore<2000:
                iconNumPlayer2=2
            elif currentBotScore<3000:
                iconNumPlayer2=3


            #Player1Frame
            player1Frame = tk.Frame(frame, bg=ss.COLORS["HIGHLIGHT_YELLOW"])
            player1Name = tk.Label(
                                text= PlayerNames[0],
                                master=player1Frame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["TEXT_WHITE"])
            player1Score = tk.Label(
                                text= str(currentPlayerScore),
                                master=player1Frame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["ACCENT_GOLD"])
            player1Status = tk.Label(player1Frame, image=Images[f'level{iconNumPlayer1}_player1'], bg=ss.COLORS["HIGHLIGHT_YELLOW"])
            player1Name.pack(fill="x", expand=True)
            player1Score.pack(fill="x", expand=True)
            player1Status.pack(fill="x", expand=True)
            player1Frame.grid(column=0, row=0,ipadx=10, sticky=tk.W+tk.E)

            #Spacer
            spacerFrame = tk.Frame(frame, bg=ss.COLORS["MONEY_GREEN"],)
            spacer = tk.Label(
                                text= "",
                                master=spacerFrame,
                                font=ss.H1["FONT"],
                                bg=ss.COLORS["MONEY_GREEN"],
                                fg=ss.COLORS["TEXT_WHITE"])
            spacer.pack()
            spacerFrame.grid(column=1, row=0, sticky=tk.W+tk.E+tk.N+tk.S)


            #Player2Frame
            player2Frame = tk.Frame(frame, bg=ss.COLORS["DARK_MONEY_GREEN"],)
            player2Name = tk.Label(
                                text= PlayerNames[1],
                                master=player2Frame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["TEXT_WHITE"])
            player2Score = tk.Label(
                                text= str(currentBotScore),
                                master=player2Frame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["ACCENT_GOLD"])
            player2Status = tk.Label(player2Frame, image=Images[f'level{iconNumPlayer2}_player2'], bg=ss.COLORS["HIGHLIGHT_YELLOW"])
            player2Name.pack(fill="x", expand=True)
            player2Score.pack(fill="x", expand=True)
            player2Status.pack(fill="x", expand=True)
            player2Frame.grid(column=2, row=0, sticky=tk.W+tk.E)

            frame.pack(fill="x", padx=30, pady=30, ipadx=10)


            # Additional Info
            additionalInfoFrame = tk.Frame(root, bg=ss.COLORS["DARK_MONEY_GREEN"])
            additionalInfoFrame.columnconfigure(0, weight=1) # For Host Sprite
            additionalInfoFrame.columnconfigure(1, weight=3) # For Answer Status
            additionalInfoFrame.columnconfigure(2, weight=1) # For Spacing
            additionalInfoFrame.columnconfigure(3, weight=1) # For Delta Scores
            additionalInfoFrame.pack(fill="x", padx=30)

            # Bottom Spacer
            spacerBottomFrame = tk.Frame(additionalInfoFrame, bg=ss.COLORS["MONEY_GREEN"],)
            spacerBottom = tk.Label(
                                text= "",
                                master=spacerFrame,
                                font=ss.H1["FONT"],
                                bg=ss.COLORS["MONEY_GREEN"],
                                fg=ss.COLORS["TEXT_WHITE"])
            spacerBottom.pack()
            spacerBottomFrame.grid(column=2, row=0, sticky=tk.W+tk.E+tk.N+tk.S)



            host = tk.Label(additionalInfoFrame,image = Images["host"], bg=ss.COLORS["HIGHLIGHT_YELLOW"], borderwidth=1)
            host.grid(column=0, row=0, sticky="w")

            if isGameOngoing:
                questionStatus = tk.Label(
                                text= f"{currentContestant} {answerStatus}",
                                master=additionalInfoFrame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["ACCENT_GOLD"],
                                justify="left")
                questionStatus.grid(column=1, row=0, sticky="w")
                if isLastAnswerCorrect:
                    winSound = choice(Sounds["correct"])
                    mixer.Channel(1).play(mixer.Sound(winSound))
                else:
                    loseSound = choice(Sounds["wrong"])
                    mixer.Channel(1).play(mixer.Sound(loseSound))
            else:
                winner = ""
                if currentPlayerScore > currentBotScore:
                    winner = f"{PlayerNames[0]} WON!"
                    mixer.Channel(1).play(mixer.Sound("Player1Won.wav"))
                elif currentPlayerScore == currentBotScore:
                    winner = "IT'S A TIE"
                else:
                    winner = f"{PlayerNames[1]} WON!"
                    mixer.Channel(1).play(mixer.Sound("Player2Won.wav"))
                questionStatus = tk.Label(
                                text= f"{winner}",
                                master=additionalInfoFrame,
                                font=ss.H1["FONT"],
                                bg=ss.H1["BACKGROUND_COLOR"],
                                fg=ss.COLORS["ACCENT_GOLD"],
                                justify="left")
                questionStatus.grid(column=1, row=0, sticky="w")

            questionStatus = tk.Label(
                                text= f'''{PlayerNames[0]}: {playerScoreDeltaAsText} \n {PlayerNames[1]}: {botScoreDeltaAsText}''',
                                master=additionalInfoFrame,
                                font=ss.H2["FONT"],
                                bg=ss.COLORS["TEXT_WHITE"],
                                fg=ss.COLORS["TEXT_BLACK"])
            questionStatus.grid(column=3, row=0)


    def process():
        '''
        changes whose turn it is and updates previousScore variable
        -> no return value
        developer-in-charge: mayo
        '''
        global currentPlayerScore
        global previousPlayerScore
        global isPlayerMove
        global currentScene
        global previousBotScore
        global currentBotScore
        global currentQuestion
        global goldenQuestions
        global ENVIRONMENT

        # Switch Turns
        if nextScene != "GOLDEN_QUESTION_SHOWING":
            if isPlayerMove:
                isPlayerMove = False
            else:
                isPlayerMove = True
        else:
            currentQuestion = choice(goldenQuestions)
            goldenQuestions.pop(goldenQuestions.index(currentQuestion))
            currentQuestion["isGolden"] = False


        previousPlayerScore = currentPlayerScore
        previousBotScore = currentBotScore
        # Changes Scene based on ENVIRONMENT:
        if ENVIRONMENT=="COLAB":
            change_scene_to(nextScene)
        else:
            if nextScene == "GOLDEN_QUESTION_SHOWING":
                do_golden_question()
            else:
                do_question_select()



class EndPage(Page):
    '''
    displays the final page and declares the winner
    developer-in-charge: samonte

    Attributes
    ----------
    None: None
    '''

    def run():
        pass

    def render():
        pass

    def process():
        pass


class GoldenQuestion(Page):
    '''
    displays the golden question
    developer-in-charge: samonte

    Attributes
    ----------
    None: None
    '''

    def run():
        '''
        renders the golden question, allows bot to move
        developer-in-charge: mayo
        '''
        render_golden_question_card()
        if (not isPlayerMove) and (gameDifficulty!='PVP'): #If bot's move, choose an answer
            answerStatus = get_bot_answer_to_question_notebook()   # Gets the user's input for the question parameters
            root.after(1500, lambda: update_info_from_golden_question_showing("IrrelevantArg", answerStatus))

    def render():
        '''
        prints the golden question and relevant parameters
        ->no return value
        developer-in-charge: Cheska
        '''
        global currentQuestion
        global PlayerNames
        global ENVIRONMENT
        global Images

        questionText = currentQuestion["Question"]
        questionChoices = currentQuestion["Choices"]

        if isPlayerMove:
            questionForWhom = PlayerNames[0]
        else:
            questionForWhom = PlayerNames[1]

        if ENVIRONMENT == "COLAB":
            output.clear()

            # Prints the question, bid value, and choices with formatting
            print(f"======={questionForWhom}: GOLDEN QUESTION =======")
            print("QUESTION: ")
            print(f" {questionText}")
            print("")
            print("CHOICES: ")
            for choice in questionChoices:
                print(choice)
            print("")

        else: #FOR NOTEBOOK ENVIRONMENTS
            # Clear Screen
            clear_notebook_screen()

            # Display Bacground Image
            background = tk.Label(root,image = Images['backgroundImage'])
            background.place(x=0, y=0)

            #Display Header
            header = tk.Label(
                            text=f"======= For {questionForWhom}: GOLDEN QUESTION =======",
                            font = ss.H2["FONT"],
                            fg= ss.H2["FONT_COLOR"],
                            bg= ss.H2["BACKGROUND_COLOR"])
            header.pack(pady=45)

            #Display Question
            header = tk.Label(text=f" {questionText}", font = (FONT[0], 30), wraplength=1000, height=4, bg="#F5E6CA", fg="#343F56")
            header.pack(pady=5)

            #Spacer
            spacer = tk.Frame()
            spacer.pack(pady=5)

            #Display Options
            for choice in questionChoices:
                answerButton = tk.Button(text=choice, font=(FONT[0], 20), command=lambda answer=choice[0]: get_user_answer_to_question(answer, True))
                answerButton.pack(pady=10, fill="x")

            if (not isPlayerMove) and (gameDifficulty!="PVP"):
                answerButton.configure(state="disabled") #Disabled when bot's move

    def process():
        '''
        updates the currentScore is answer is correct
        -> no return value
        developer-in-charge: mayo
        '''
        global isLastAnswerCorrect
        global currentPlayerScore
        global lastBidValue
        global current
        global isPlayerMove
        global currentBotScore
        global currentQuestion

        isLastAnswerCorrect = isAnswerCorrect
        # Updates player score
        if isPlayerMove:
            if isAnswerCorrect:
                isLastAnswerCorrect = True
                currentPlayerScore += abs(currentBotScore//2)
                currentBotScore -= abs(currentBotScore//2)
        else:
            if isAnswerCorrect:
                isLastAnswerCorrect = True
                currentBotScore += abs(currentPlayerScore//2)
                currentPlayerScore -= abs(currentPlayerScore//2)

        # Changes Scene based on Environment
        if ENVIRONMENT == "COLAB":
            change_scene_to(nextScene)
        else:
            do_score_showing()


# Agent Classes -----------------------------
class Contestant(ABC):
    """
    Contestants are agents that have scores, a name, and can win.

    Developer-in-Charge: 

    Attributes
    ----------
    example: data_type
        Description
    """

class Bot(ABC):
    """
    Bots are agents that can answer and get questions without player
    input.

    Developer-in-Charge: 

    Attributes
    ----------
    example: data_type
        Description
    """

from abc import ABC, abstractmethod
from random import choice

# Abstract Classes
class Contestant(ABC):
  """
    A class to represent a contestant for the game.

    Attributes
    ----------
    name : str
        name to be displayed in the score
    score : int
        the number of points a contestant has
  """

  def __init__(self, name, score):
    """
    Sets the necessary attributes for the contestants

    Parameters
    ----------
        name : str
            name to be displayed in the score
        score : int
            the number of points a contestant has
    """
    self.name = name
    self.score = score

  def get_half_the_points(self, opponent):
    """
    Transfers half the oppponent's score to this object.

    Parameters
    ----------
        opponent : Contestant Sub.
            Reference to the opponent object to get score from
    """
    opponentHalfScore = opponent.score // 2
    opponent.score -= opponentHalfScore
    self.score += opponentHalfScore

  def __str__(self):
    """
    returns contestant name and score to be printed
    """
    return f"{self.name}: {self.score}"

class Bot(ABC):
  """
    An abstract class to represent a "bot", objects able to act like a player without user input
  """
  @abstractmethod
  def choose_random_question():
    """
    Chooses a random question from currentQuestions
    """
    pass

  @abstractmethod
  def choose_answer_result():
    """
    Returns true and calls Contestant.get_half_the_points() if bot should get the answer correct,
    only returns false otherwise
    """
    pass

# Players Classes
class Player(Contestant):
    """
    A Contestant Sub-Class that can accept user input
    """
    pass

class StandardBot(Contestant, Bot): #Multiple Inheritance
    """
    A Contestant and Bot sub-class that answers randomly based on difficulty

    Attributes
    ----------
    difficulty : str
        qualitative description of the difficulty
    """
    
    def set_difficulty(self, difficulty):
        """
        setter method that sets the difficulty attribute of the object

        Parameters
        ----------
        difficulty : str
           qualitative description of the difficulty
        """
        assert difficulty in ["easy", "medium", "hard"]
        self.__difficulty = difficulty

    def choose_random_question(self, questions):
        """
        randomly chooses a question from a list

        Parameters
        ----------
        questions: list[str]
            list of questions to choose from
        """
        return choice(questions)

    def choose_answer_result(self, opponent, currentQuestion):
        """
        randomly chooses to answer correctly or not based on difficulty
        calls a method to transfer half the points if answering correctly

        Parameters
        ----------
        opponent : Contestant Sub.
            Reference to the opponent object to get score from
        currentQuestion : str
            the current question being asked
        """
        result = False
        difficulty = self.__difficulty
        match difficulty:
            case "easy":
                result = choice([False, False, True])
            case "medium":
                result = choice([False, False, True])
            case "hard":
                result = True
        if result:
            self.get_half_the_points(opponent)
        return result

class GeekBot(Contestant, Bot):
    """
    A Contestant and Bot sub-class that answers randomly, but with preference to its specialty.
    It often gets questions that match its specialty correctly. Answers randomly otherwise
    ...

    Inherited Attributes
    ----------
    name : str
        name to be displayed in the score
    score : int
        the number of points a contestant has

    Attributes
    ----------
    specialty : str
        a specialty taken from the list of currentQuestions to be preferred by the bot
    """
    def set_specialty(self, specialty):
        """
        setter method that sets the specialty attribute of the object

        Parameters
        ----------
        specialty : str
           a specialty taken from the list of currentQuestions to be preferred by the bot
        """
        assert specialty in ["Science", "Math", "History", "Business"]
        self.__specialty = specialty

    def choose_random_question(self, questions):
        """
        returns the question preferred by the bot based on its specialty

        Parameters
        ----------
        questions : list of str
           the list of possible questions
        """
        return self.__specialty

    def choose_answer_result(self, opponent, currentQuestion):
        """
        randomly chooses to answer correctly or not based on bot specialty
        calls a method to transfer half the points if answering correctly

        Parameters
        ----------
        opponent : Contestant Sub.
            Reference to the opponent object to get score from
        currentQuestion : str
            the current question being asked
        """
        result = False
        if self.__specialty == currentQuestion:
            result = choice([False, True, True])
        else:
            result = choice([False, False, True])

        if result:
            self.get_half_the_points(opponent)
        return result

class HelperBot(Bot):
    """
    A subclass of Bot that represents a helper bot in the game.

    This bot assists the player by providing the correct answer to the question,
    but it is accurate only 75% of the time.
    """

class StudentBot(StandardBot):
    """
    A subclass of StandardBot that represents a bot capable of playing a game.

    This bot inherits basic functionalities from StandardBot and implements
    a mechanism to increase the game's difficulty as time progresses.

    Attributes:
    - difficulty (int): Represents the current difficulty level of the game.

    Methods:
    - difficultyRamp(difficultyPerInterval: int, interval: int):
        Sets the parameters for the difficulty increase over intervals.
    - set_difficulty_ramp(difficultyRamp: (int, int)):
        Sets the difficulty increase parameters using a tuple.
    """

class RiddlerBot(Bot, Contestant):
    """
    A subclass of Bot and Contestant that represents a cheater bot in the game.

    This bot takes two sequential turns, steals points randomly, and gains points
    even if the answer is wrong.
    """

# Factory Class -----------------------------
class ContestantFactory:
    pass

# Mediator Class -----------------------------

class TurnMediator():
    """
    Mediator for handling interactions between pages and agents

    Developer-in-Charge: Paolo Mayo 

    Attributes
    ----------
    turnOrder: List[type[Contestant]]
        Determines whose turn it is in a round
    turn: type[Contestant]
        Determines whose turn it is in a round
    """
    
    def __init__(self, turnOrder:list[type[Contestant]], turn:type[Contestant])->None:
        self.turnOrder = turnOrder
        self.turn = turn
    

    def get_question(self):
        """
        Gets a question based on whose turn it is

        Developer-in-Charge: Paolo Mayo 
        
        Attributes
        ----------
        self

        Return
        ----------
        None: None
        """
        pass

    def get_answer(self):
        """
        Gets an answer status based on whose turn it is

        Developer-in-Charge: Paolo Mayo 

        Attributes
        ----------
        self

        Return
        ----------
        None: None
        """
        pass

    def next_turn(self):
        """
        Changes the turn based on an order

        Developer-in-Charge: Paolo Mayo 

        Parameters
        ----------
        self

        Return
        ----------
        None: None
        """
        pass


def main()->None:
    '''
    starts the game loop
    '''
    #Initialize Global Var Class
    gameState = GameState()

    #Initialize Moderator

    #Initialize all page classes
    menu = MenuPage()
    menu.run(gameState)
main()
print("AAA")