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
from random import choice
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

    @abstractmethod #hello
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

    def change_page():
        '''
        calls the next page and clears the output
        '''
        pass


class IntroPage(Page):
    '''
    displays the very first screen you see
    developer-in-charge: Samuel Samonte

    Attributes
    ----------
    None: None
    '''

    def run(self):
        self.render()    # Renders the instructions to the game

    def render():
        pass

    def process():
        pass


class MenuPage(Page):
    '''
    displays the main menu
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


class QuestionBoardPage(Page):
    '''
    displays the board with all of the bid values
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


class QuestionCardPage(Page):
    '''
    displays the question itself
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


class ScoreBoardPage(Page):
    '''
    displays the scoreboard
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
        pass

    def render():
        pass

    def process():
        pass


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

    #Initialize all

print("AAA")